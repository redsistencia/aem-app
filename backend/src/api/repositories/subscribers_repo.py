from sqlalchemy.orm import Session
from models.subscriber import Subscriber, SubscriberCreate
    
# Obtener usuario por email
def get_subscriber_by_email(db: Session, email: str) -> Subscriber | None:
    return db.query(Subscriber).filter(Subscriber.email == email).first()

# Crea una nueva fila en la tabla activities
def create_subscriber(db: Session, subscriber_data: SubscriberCreate):
    data_dict = subscriber_data.dict()          # Convierte el Pydantic model a dict
    new_subscriber = Subscriber(**data_dict)    # Crear la instancia de Activity con ** unpacking
    db.add(new_subscriber)                      # Agregar a la sesión de la DB  
    db.commit()                                 # db.commit() guarda cambios
    db.refresh(new_subscriber)                  # db.refresh() actualiza el objeto con los datos finales de la DB
    return new_subscriber