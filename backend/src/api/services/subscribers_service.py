from sqlalchemy.orm import Session
from models.subscriber import SubscriberCreate
from repositories.subscribers_repo import create_subscriber, get_subscriber_by_email

# Crear un nuevo suscriptor
def create_subscriber_service(db: Session, subscriber: SubscriberCreate):
    if get_subscriber_by_email(db, subscriber.email):
        raise ValueError("Email already registered")        # Error si el email ya está registrado
    return create_subscriber(db, subscriber)

