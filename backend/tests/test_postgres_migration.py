"""Run only against an empty, disposable PostgreSQL database supplied by the caller."""
import os
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from src.api.main import app
from src.api.models.user import User, UserRole
from src.api.security.auth import create_access_token
from src.api.security.hash import hash_password
from src.db.base import Base
from src.db.models.activity import Activity
from src.db.session import get_db


@unittest.skipUnless(os.getenv('AEM_TEST_POSTGRES_URL'), 'Requires a disposable PostgreSQL database')
class PostgresMigrationTests(unittest.TestCase):
    def test_upgrade_preserves_data_and_api_works(self):
        url = os.environ['AEM_TEST_POSTGRES_URL']
        engine = create_engine(url)
        self.addCleanup(engine.dispose)
        self.assertEqual(inspect(engine).get_table_names(), [], 'Use an empty, disposable database')
        config = Config(str(Path(__file__).resolve().parents[1] / 'src/api/alembic.ini'))
        with patch('src.db.session.engine', engine), patch('src.db.session.DATABASE_URL', url):
            command.upgrade(config, '72fa45b05282')
            with engine.begin() as connection:
                connection.execute(text("INSERT INTO activities (title, description, location, activity_date) VALUES ('Actividad anterior', NULL, 'Palma', '2026-12-10 18:30:00')"))
            command.upgrade(config, 'head')

        sessions = sessionmaker(bind=engine)
        with sessions() as db:
            activity = db.query(Activity).one()
            self.assertEqual(activity.slug, 'actividad-1')
            self.assertEqual(activity.date, date(2026, 12, 10))
            self.assertEqual(activity.activity_date.hour, 18)
            self.assertEqual(activity.location, 'Palma')
            self.assertEqual(activity.description, '')
            db.add(User(username='admin', email='admin@example.com', password=hash_password('test-password'), role=UserRole.admin))
            db.commit()

        def override_db():
            with sessions() as db:
                yield db

        app.dependency_overrides[get_db] = override_db
        self.addCleanup(app.dependency_overrides.clear)
        headers = {'Authorization': 'Bearer ' + create_access_token({'user_email': 'admin@example.com'})}
        with TestClient(app) as client:
            self.assertEqual(client.get('/activities/actividad-1').status_code, 200)
            response = client.post('/admin/activities/', json={
                'title': 'Actividad nueva', 'description': 'Encuentro en Palma',
                'date': '2026-12-11', 'slug': 'actividad-nueva',
            }, headers=headers)
            self.assertEqual(response.status_code, 201, response.text)
            response = client.post('/subscribers/', json={
                'name': 'Daniela', 'lastname': 'Pérez', 'email': 'socia@example.com',
                'privacy_policy': True, 'document_id': 'AB12345', 'newsletter': True,
            })
            self.assertEqual(response.status_code, 201, response.text)
            response = client.post('/subscribers/unsubscribe', json={
                'email': 'socia@example.com', 'document_id': 'AB12345',
            })
            self.assertEqual(response.status_code, 200, response.text)

        with engine.connect() as connection:
            differences = compare_metadata(MigrationContext.configure(connection), Base.metadata)
            self.assertEqual(differences, [])
