from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from models.subscriber import SubscriberCreate, SubscriberRead, SubscriberUpdate
from services.subscribers_service import create_subscriber_service, update_subscriber_service, get_subscriber_service, delete_subscriber_service
from db.session import get_db
from security.auth import require_role

# Inicializa el router de FastAPI para las suscripciones
router = APIRouter()

# Endpoint para obtener todos los subscribers
@router.get("/admin/subscribers", response_model=list[SubscriberRead])
def get_all_subscribers(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")) # Control de acceso por rol
) -> list[SubscriberRead]:
    # Devuelve la lista de todos los suscriptores
    return get_subscriber_service(db, None)

# Endpoint para obtener un subscriber por email o ID
@router.get("/admin/subscriber/{entry}", response_model=SubscriberRead)
def get_subscriber_endpoint(
    entry: str,                     # ID o email del suscriptor
    db: Session = Depends(get_db),   # Sesión de base de datos
    user: User = Depends(require_role("admin")) # Control de acceso por rol
) -> SubscriberRead:
    return get_subscriber_service(db, entry)

# Endpoint para crear un nuevo suscriptor
@router.post("/subscribe", response_model=SubscriberRead)
def create_subscriber_endpoint(
    subscriber: SubscriberCreate,   # Datos del suscriptor (email, nombre, etc.)
    db: Session = Depends(get_db)    # Sesión de base de datos
) -> SubscriberRead:
    # Registra el suscriptor en la base de datos
    return create_subscriber_service(db, subscriber)

# Endpoint para actualizar parcialmente un subscriber
@router.patch("/admin/subscribe/{subscriber_id}", response_model=SubscriberRead)
def update_subscriber_endpoint(
    subscriber_id: int,                            # ID del suscriptor a actualizar
    subscriber_data: SubscriberUpdate,             # Datos a actualizar (parciales)
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user: User = Depends(require_role("admin")) # Control de acceso por rol
) -> SubscriberUpdate:
    # Actualiza solo los campos enviados en la petición
    updated_subscriber = update_subscriber_service(
        db,
        subscriber_id,
        subscriber_data.model_dump(exclude_unset=True)     # Excluye campos no enviados
    )
    return updated_subscriber

#Endpoint para eliminar un subscriber
@router.delete("/admin/subscribe/{entry}", response_model=dict)
def delete_subscriber_endpoint(
    entry: str | int,                                    # ID o email del suscriptor a eliminar
    db: Session = Depends(get_db),                       # Sesión de base de datos
    user: User = Depends(require_role("admin"))          # Solo admin puede eliminar suscriptores
) -> dict[str, str]:
    return delete_subscriber_service(db, entry)