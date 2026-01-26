from typing import Any
from sqlalchemy.orm import Session
from models.subscriber import Subscriber, SubscriberCreate, SubscriberUpdate

# Obtener usuario por ID o email
def get_subscriber(db: Session, subscriber_entry: str | int | None) -> Subscriber | list[Subscriber] | None:
    # Si es int → buscar por ID
    if isinstance(subscriber_entry, int):
        return db.query(Subscriber).filter(Subscriber.id == subscriber_entry).first()
    # Si es str -> buscar por email
    if isinstance(subscriber_entry, str):
        return db.query(Subscriber).filter(Subscriber.email == subscriber_entry).first()
    # Cualquier otro tipo no soportado → devolver todos
    return db.query(Subscriber).all()

# Crea una nueva fila en la tabla subscribers
def create_subscriber(db: Session, subscriber_data: SubscriberCreate) -> Subscriber:
    data_dict = subscriber_data.model_dump()            # Convierte el Pydantic model a model de Python
    new_subscriber = Subscriber(**data_dict)            # Crear la instancia de Subscriber con ** unpacking
    db.add(new_subscriber)                              # Agregar a la sesión de la DB  
    db.commit()                                         # db.commit() guarda cambios
    db.refresh(new_subscriber)                          # db.refresh() actualiza el objeto con los datos finales de la DB
    return new_subscriber


def update_subscriber(db: Session, subscriber: SubscriberUpdate, data: dict[str, Any]) -> SubscriberUpdate:   
    # Actualización dinámica de campos
    for key, value in data.items():
        setattr(subscriber, key, value)

    db.commit()                    # db.commit() guarda cambios
    db.refresh(subscriber)         # db.refresh() actualiza el objeto con los datos finales de la DB
    return subscriber


def delete_subscriber(db: Session, subscriber: Subscriber) -> bool:  
    db.delete(subscriber)      # Eliminarla
    db.commit()                # Confirmar cambios en la DB
    return True