from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.activity import ActivityRead, ActivityUpdate, ActivityCreate
from db.session import get_db
from models.user import User
from security.auth import require_role
from services.activities_service import (
    create_activity_service,
    read_activities_service,
    delete_activity_service,
    update_activity_service
)

# Inicializa el router de FastAPI para las rutas de actividades
router = APIRouter()


# Endpoint para obtener todas las actividades
@router.get("/admin/activities", response_model=list[ActivityRead])
def get_all_activities(
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user: User = Depends(require_role("admin", "editor")) # Solo admin y editor pueden acceder
) -> list[ActivityRead]:
    # Devuelve la lista de actividades desde el servicio
    return read_activities_service(db, activity_id=None)

# Endpoint para obtener una actividad en concreto
@router.get("/admin/activity/{activity_id}", response_model=ActivityRead)
def get_activity_endpoint(
    activity_id: int,                              # ID de la actividad a obtener
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user: User = Depends(require_role("admin", "editor")) # Solo admin y editor pueden acceder
) -> ActivityRead:
    # Devuelve la lista de actividades desde el servicio
    return read_activities_service(db, activity_id)

# Endpoint para crear una nueva actividad
@router.post("/admin/activities/", response_model=ActivityRead)
def create_activity_endpoint(
    activity_data: ActivityCreate,                 # Datos de la nueva actividad
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user: User = Depends(require_role("admin"))          # Solo admin puede crear actividades
) -> ActivityRead:
    # Llama al servicio que crea la actividad
    return create_activity_service(db, activity_data)

# Endpoint para actualizar parcialmente una actividad
@router.patch("/admin/activities/{activity_id}", response_model=ActivityRead)
def update_activity_endpoint(
    activity_id: int,                              # ID de la actividad a actualizar
    activity_data: ActivityUpdate,                 # Datos a actualizar (parciales)
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user: User = Depends(require_role("admin", "editor")) # Control de acceso por rol
) -> ActivityRead:
    # Actualiza solo los campos enviados en la petición
    updated_activity = update_activity_service(
        db,
        activity_id,
        activity_data.model_dump(exclude_unset=True)     # Excluye campos no enviados
    )
    return updated_activity

# Endpoint para eliminar una actividad por su ID
@router.delete("/admin/activities/{activity_id}")
def delete_activity_endpoint(
    activity_id: int,                              # ID de la actividad a eliminar
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user: User = Depends(require_role("admin", "editor")) # Control de acceso por rol
) -> dict[str, str]:
    # Llama al servicio que elimina la actividad
    return delete_activity_service(db, activity_id)