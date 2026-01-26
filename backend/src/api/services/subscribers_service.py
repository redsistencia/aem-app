from datetime import datetime
from realtime import Any
from sqlalchemy.orm import Session
import re
from exceptions.subscriber_exceptions import SubscriberExists, SubscriberNotFound, SubscriberErrorDateFormat, SubscriberEmailInvalid
from models.subscriber import Subscriber, SubscriberCreate, SubscriberUpdate
from repositories.subscribers_repo import create_subscriber, update_subscriber, get_subscriber, delete_subscriber

# Crear un nuevo suscriptor
def create_subscriber_service(db: Session, subscriber: SubscriberCreate) -> Subscriber:
    if get_subscriber(db, subscriber.email):
        raise SubscriberExists()                            # Error si el email ya está registrado
    return create_subscriber(db, subscriber)

# Obtener un suscriptor por ID o email
def get_subscriber_service(
    db: Session,
    subscriber_entry: str | int | None
) -> Subscriber | list[Subscriber]:

    # Si no se pasa nada → devolver todos
    if subscriber_entry is None:
        return get_subscriber(db, None)

    # Si es string y contiene solo dígitos → convertir a int
    if isinstance(subscriber_entry, str) and subscriber_entry.isdigit():
        subscriber_entry = int(subscriber_entry)

    # Si sigue siendo string → validar email
    if isinstance(subscriber_entry, str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", subscriber_entry):
            raise SubscriberEmailInvalid()

    subscriber = get_subscriber(db, subscriber_entry)
    if not subscriber:
        raise SubscriberNotFound()

    return subscriber


# Actualizar una actividad existente
def update_subscriber_service(db: Session, subscriber_id: int, data: dict[str, Any]) -> SubscriberUpdate:
    # Obtener la actividad existente
    subscriber = get_subscriber(db, subscriber_id)
    if not subscriber:
        raise SubscriberNotFound()
    # Comprobar si se envió la fecha de la actividad
    if "termination_date" in data:
        # Obtener la fecha de terminación
        termination_date = data["termination_date"]
        # Convertir a datetime si viene como string
        if isinstance(termination_date, str):
            try:
                termination_date = datetime.fromisoformat(termination_date)
            except ValueError:
                raise SubscriberErrorDateFormat()
        # Guardar la fecha convertida
        data["termination_date"] = termination_date
    # Actualizar la actividad en el repositorio
    return update_subscriber(db, subscriber, data)

# Eliminar un suscriptor por ID o email
def delete_subscriber_service(db: Session, entry: str | int) -> dict[str, str]:
    subscriber = get_subscriber(db, entry)
    if not subscriber:
        raise SubscriberNotFound()
    # Eliminar el suscriptor
    delete_subscriber(db, subscriber)
    return {"message": "Suscriptor eliminado exitosamente"}