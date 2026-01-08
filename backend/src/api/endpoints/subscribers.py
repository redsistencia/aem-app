from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.subscriber import SubscriberCreate, SubscriberRead
from services.subscribers_service import create_subscriber_service
from db.session import get_db

# Inicializa el router de FastAPI para las suscripciones
router = APIRouter()


# Endpoint para crear un nuevo suscriptor
@router.post("/subscribe", response_model=SubscriberRead)
def create_subscriber_endpoint(
    subscriber: SubscriberCreate,   # Datos del suscriptor (email, nombre, etc.)
    db: Session = Depends(get_db)    # Sesión de base de datos
):
    # Registra el suscriptor en la base de datos
    return create_subscriber_service(db, subscriber)
