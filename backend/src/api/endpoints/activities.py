from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.activity import ActivityRead, ActivityUpdate, ActivityCreate
from db.session import get_db
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
def get_activities_endpoint(
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user = Depends(require_role("admin", "editor")) # Solo admin y editor pueden acceder
):
    # Devuelve la lista de actividades desde el servicio
    return read_activities_service(db)


# Endpoint para eliminar una actividad por su ID
@router.delete("/admin/activities/{activity_id}")
def delete_activity_endpoint(
    activity_id: int,                              # ID de la actividad a eliminar
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user = Depends(require_role("admin", "editor")) # Control de acceso por rol
):
    # Llama al servicio que elimina la actividad
    return delete_activity_service(db, activity_id)


# Endpoint para actualizar parcialmente una actividad
@router.patch("/admin/activities/{activity_id}", response_model=ActivityRead)
def update_activity_endpoint(
    activity_id: int,                              # ID de la actividad a actualizar
    activity_data: ActivityUpdate,                 # Datos a actualizar (parciales)
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user = Depends(require_role("admin", "editor")) # Control de acceso por rol
):
    # Actualiza solo los campos enviados en la petición
    updated_activity = update_activity_service(
        db,
        activity_id,
        activity_data.dict(exclude_unset=True)     # Excluye campos no enviados
    )
    return updated_activity


# Endpoint para crear una nueva actividad
@router.post("/admin/activities/", response_model=ActivityRead)
def create_activity_endpoint(
    activity_data: ActivityCreate,                 # Datos de la nueva actividad
    db: Session = Depends(get_db),                 # Sesión de base de datos
    user = Depends(require_role("admin"))          # Solo admin puede crear actividades
):
    # Llama al servicio que crea la actividad
    return create_activity_service(db, activity_data)
