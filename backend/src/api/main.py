from fastapi import FastAPI
from endpoints import users, subscribers, activities
from models.user import Base as UserBase
from models.subscriber import Base as SubscriberBase
from models.activity import Base as ActivityBase
from db.session import engine
from db.base import Base


# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema SQLAlchemy + Supabase")

app.include_router(users.router)
app.include_router(subscribers.router)
app.include_router(activities.router)
