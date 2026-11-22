"""Regression tests run against an isolated SQLite database, without external services."""
import os
import unittest
from datetime import date
from tempfile import NamedTemporaryFile
from unittest.mock import patch

os.environ['DEBUG'] = 'false'
os.environ['DATABASE_URL'] = 'sqlite://'
os.environ['SECRET_KEY'] = 'test-only-secret-do-not-use-in-production'

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.api.models.subscriber import Subscriber
from src.api.models.user import User, UserRole
from src.api.security.auth import create_access_token
from src.api.security.hash import hash_password, verify_password
from src.core.config import Settings, settings
from src.db.base import Base
from src.db.models.activity import Activity
from src.db.session import get_db

PASSWORD = 'test-password-123'
PASSWORD_HASH = hash_password(PASSWORD)


class ApiRegressionTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine)
        with self.sessions() as db:
            db.add_all([
                User(username='admin', email='admin@example.com', password=PASSWORD_HASH, role=UserRole.admin),
                User(username='editor', email='editor@example.com', password=PASSWORD_HASH, role=UserRole.editor),
                User(username='inactive', email='inactive@example.com', password=PASSWORD_HASH, role=UserRole.admin, active=False),
            ])
            db.commit()

        def override_db():
            with self.sessions() as db:
                yield db

        app.dependency_overrides[get_db] = override_db
        self.client = TestClient(app)
        self.headers = self.auth('admin@example.com')
        self.activity = {
            'title': 'Una actividad con más de treinta caracteres',
            'description': 'Encuentro de la comunidad',
            'date': '2026-12-10',
            'slug': 'mateada-comunitaria',
        }
        self.subscriber = {
            'name': 'Daniela', 'lastname': 'Pérez', 'email': 'socia@example.com',
            'privacy_policy': True, 'document_id': 'AB12345',
        }

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def auth(self, email, **claims):
        token = create_access_token({'user_email': email, 'role': 'admin', **claims})
        return {'Authorization': f'Bearer {token}'}

    def test_health_and_cors(self):
        self.assertEqual(self.client.get('/health').json(), {'status': 'ok'})
        response = self.client.options('/subscribers/', headers={
            'Origin': settings.frontend_url.rstrip('/'),
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['access-control-allow-origin'], settings.frontend_url.rstrip('/'))

    def test_login_and_session(self):
        response = self.client.post('/admin/users/login', json={'email': 'ADMIN@example.com', 'password': PASSWORD})
        self.assertEqual(response.status_code, 200, response.text)
        me = self.client.get('/admin/users/me', headers={'Authorization': f"Bearer {response.json()['access_token']}"})
        self.assertEqual(me.json()['email'], 'admin@example.com')
        self.assertNotIn('password', me.json())

    def test_swagger_login_and_protected_request(self):
        response = self.client.post('/admin/users/token', data={
            'username': 'ADMIN@example.com', 'password': PASSWORD, 'grant_type': 'password',
        })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['token_type'], 'bearer')
        headers = {'Authorization': f"Bearer {response.json()['access_token']}"}
        self.assertEqual(self.client.get('/admin/subscribers/', headers=headers).status_code, 200)
        self.assertNotIn('password', response.json())

    def test_swagger_rejects_invalid_credentials(self):
        for email, password in [
            ('admin@example.com', 'wrong'), ('missing@example.com', PASSWORD),
            ('inactive@example.com', PASSWORD), ('invalid-email', PASSWORD),
        ]:
            with self.subTest(email=email):
                response = self.client.post('/admin/users/token', data={'username': email, 'password': password})
                self.assertEqual(response.status_code, 401, response.text)
                self.assertNotIn('access_token', response.json())

    def test_swagger_requires_form_fields_and_preserves_permissions(self):
        self.assertEqual(self.client.post('/admin/users/token', data={'username': 'admin@example.com'}).status_code, 422)
        response = self.client.post('/admin/users/token', data={'username': 'editor@example.com', 'password': PASSWORD})
        self.assertEqual(response.status_code, 200, response.text)
        headers = {'Authorization': f"Bearer {response.json()['access_token']}"}
        self.assertEqual(self.client.get('/admin/subscribers/', headers=headers).status_code, 403)

    def test_swagger_schema_points_to_form_login(self):
        schema = self.client.get('/openapi.json').json()
        flow = schema['components']['securitySchemes']['OAuth2PasswordBearer']['flows']['password']
        self.assertEqual(flow['tokenUrl'], '/admin/users/token')
        self.assertIn('application/x-www-form-urlencoded', schema['paths'][flow['tokenUrl']]['post']['requestBody']['content'])
        self.assertIn('application/json', schema['paths']['/admin/users/login']['post']['requestBody']['content'])

    def test_invalid_inactive_and_unknown_login(self):
        for email, password in [('admin@example.com', 'wrong'), ('missing@example.com', PASSWORD), ('inactive@example.com', PASSWORD)]:
            with self.subTest(email=email):
                self.assertEqual(self.client.post('/admin/users/login', json={'email': email, 'password': password}).status_code, 401)

    def test_expired_invalid_and_missing_tokens(self):
        expired = create_access_token({'user_email': 'admin@example.com'}, expires_minutes=-1)
        for headers in [{}, {'Authorization': 'Bearer invalid'}, {'Authorization': f'Bearer {expired}'}]:
            self.assertEqual(self.client.get('/admin/activities/', headers=headers).status_code, 401)

    def test_authorization_uses_current_database_role_and_status(self):
        self.assertEqual(self.client.get('/admin/subscribers/', headers=self.auth('editor@example.com')).status_code, 403)
        self.assertEqual(self.client.get('/admin/activities/', headers=self.auth('inactive@example.com')).status_code, 401)
        with self.sessions() as db:
            user = db.query(User).filter_by(email='admin@example.com').one()
            user.role = UserRole.editor
            db.commit()
        self.assertEqual(self.client.get('/admin/subscribers/', headers=self.headers).status_code, 403)

    def test_registration_uses_post_and_correct_response(self):
        data = {'username': 'new', 'email': 'new@example.com', 'password': PASSWORD, 'role': 'editor'}
        response = self.client.post('/admin/users/', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 201, response.text)
        self.assertEqual(response.json()['username'], 'new')
        self.assertNotIn('password', response.json())
        self.assertEqual(self.client.post('/admin/users/', json=data, headers=self.headers).status_code, 409)
        self.assertEqual(self.client.get('/admin/users/', headers=self.headers).status_code, 405)

    def test_oversized_password_is_validation_error(self):
        response = self.client.post('/admin/users/', json={
            'username': 'new', 'email': 'new@example.com', 'password': 'á' * 37, 'role': 'editor',
        }, headers=self.headers)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(verify_password('x' * 73, PASSWORD_HASH))

    def test_signup_defaults_and_database_persistence(self):
        response = self.client.post('/subscribers/', json=self.subscriber)
        self.assertEqual(response.status_code, 201, response.text)
        self.assertTrue(response.json()['active'])
        self.assertFalse(response.json()['newsletter'])
        with self.sessions() as db:
            subscriber = db.query(Subscriber).one()
            self.assertEqual(subscriber.lastname, 'Pérez')
            self.assertIsNone(subscriber.termination_date)

    def test_signup_requires_consent_and_valid_fields(self):
        for fields in [{'privacy_policy': False}, {'name': '  '}, {'nationality': 'x' * 31}, {'active': False}, {'email': 'invalid'}]:
            response = self.client.post('/subscribers/', json={**self.subscriber, **fields})
            self.assertEqual(response.status_code, 422, response.text)
        self.assertEqual(self.client.get('/admin/subscribers/', headers=self.headers).json(), [])

    def test_duplicate_email_is_case_insensitive(self):
        self.client.post('/subscribers/', json=self.subscriber)
        response = self.client.post('/subscribers/', json={**self.subscriber, 'email': 'SOCIA@example.com'})
        self.assertEqual(response.status_code, 409, response.text)
        self.assertEqual(len(self.client.get('/admin/subscribers/', headers=self.headers).json()), 1)

    def test_unsubscribe_verifies_identity_and_stops_newsletter(self):
        self.client.post('/subscribers/', json={**self.subscriber, 'newsletter': True})
        self.assertEqual(self.client.post('/subscribers/unsubscribe', json={'email': self.subscriber['email'], 'document_id': 'wrong'}).status_code, 400)
        with self.sessions() as db:
            self.assertTrue(db.query(Subscriber).one().active)
        for _ in range(2):
            response = self.client.post('/subscribers/unsubscribe', json={'email': 'SOCIA@example.com', 'document_id': 'ab12345'})
            self.assertEqual(response.status_code, 200, response.text)
        with self.sessions() as db:
            subscriber = db.query(Subscriber).one()
            self.assertFalse(subscriber.active)
            self.assertFalse(subscriber.newsletter)
            self.assertIsNotNone(subscriber.termination_date)

    def test_subscriber_update_and_numeric_delete(self):
        subscriber = self.client.post('/subscribers/', json=self.subscriber).json()
        url = f"/admin/subscribers/{subscriber['id']}"
        self.assertEqual(self.client.patch(url, json={'name': None}, headers=self.headers).status_code, 422)
        self.assertEqual(self.client.patch(url, json={'id': 99}, headers=self.headers).status_code, 422)
        response = self.client.patch(url, json={'name': 'Nuevo nombre'}, headers=self.headers)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.client.delete(url, headers=self.headers).status_code, 200)
        self.assertEqual(self.client.get(url, headers=self.headers).status_code, 404)

    def test_activity_empty_lists_and_missing_id(self):
        self.assertEqual(self.client.get('/admin/activities/', headers=self.headers).json(), [])
        self.assertEqual(self.client.get('/activities/').json(), [])
        self.assertEqual(self.client.get('/admin/activities/0', headers=self.headers).status_code, 404)

    def test_create_update_read_delete_activity(self):
        response = self.client.post('/admin/activities/', json=self.activity, headers=self.headers)
        self.assertEqual(response.status_code, 201, response.text)
        activity_id = response.json()['id']
        public = self.client.get(f"/activities/{self.activity['slug']}")
        self.assertEqual(public.status_code, 200, public.text)
        self.assertEqual(public.json()['date'], '2026-12-10')
        self.assertEqual(public.json()['title'], self.activity['title'])
        response = self.client.patch(f'/admin/activities/{activity_id}', json={'date': '2026-12-11'}, headers=self.headers)
        self.assertEqual(response.status_code, 200, response.text)
        with self.sessions() as db:
            self.assertEqual(db.get(Activity, activity_id).date, date(2026, 12, 11))
        self.assertEqual(self.client.delete(f'/admin/activities/{activity_id}', headers=self.headers).status_code, 200)
        self.assertEqual(self.client.get(f"/activities/{self.activity['slug']}").status_code, 404)

    def test_activity_validations_and_editor_permissions(self):
        for fields in [{'title': ' '}, {'title': 'x' * 151}, {'description': 'x' * 451}, {'date': 'not-a-date'}, {'slug': '\"><script>'}]:
            self.assertEqual(self.client.post('/admin/activities/', json={**self.activity, **fields}, headers=self.headers).status_code, 422)
        self.assertEqual(self.client.post('/admin/activities/', json=self.activity, headers=self.auth('editor@example.com')).status_code, 403)
        activity_id = self.client.post('/admin/activities/', json=self.activity, headers=self.headers).json()['id']
        self.assertEqual(self.client.patch(f'/admin/activities/{activity_id}', json={'date': None}, headers=self.headers).status_code, 422)
        self.assertEqual(self.client.patch(f'/admin/activities/{activity_id}', json={'title': 'Editado'}, headers=self.auth('editor@example.com')).status_code, 200)

    def test_duplicate_slug_rolls_back(self):
        self.client.post('/admin/activities/', json=self.activity, headers=self.headers)
        self.assertEqual(self.client.post('/admin/activities/', json=self.activity, headers=self.headers).status_code, 409)
        second = self.client.post('/admin/activities/', json={**self.activity, 'slug': 'segunda'}, headers=self.headers).json()
        response = self.client.patch(f"/admin/activities/{second['id']}", json={'slug': self.activity['slug']}, headers=self.headers)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.client.get('/activities/segunda').status_code, 200)


class ConfigurationTests(unittest.TestCase):
    def test_database_user_does_not_use_operating_system_user(self):
        with NamedTemporaryFile(mode='w+', suffix='.env') as env_file:
            env_file.write('user=database_user\npassword=database_password\n')
            env_file.flush()
            with patch.dict(os.environ, {'USER': 'operating_system_user'}, clear=True):
                config = Settings(_env_file=env_file.name, secret_key='test')
                self.assertEqual(config.db_user, 'database_user')

    def test_database_url_override(self):
        config = Settings(_env_file=None, database_url='sqlite://', secret_key='test')
        self.assertEqual(config.sqlalchemy_url, 'sqlite://')

    def test_database_credentials_are_escaped(self):
        config = Settings(_env_file=None, database_url=None, db_user='user@name', db_password='p@ss:/?#%', secret_key='test')
        parsed = make_url(config.sqlalchemy_url)
        self.assertEqual(parsed.username, 'user@name')
        self.assertEqual(parsed.password, 'p@ss:/?#%')
        self.assertNotIn('sslmode', parsed.query)


if __name__ == '__main__':
    unittest.main()
