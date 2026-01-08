from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.activity import ActivityCreate
from datetime import datetime
from repositories.activities_repo import (
    read_activities as read_activities_repo,
    delete_activity,
    update_activity,
    create_activity
)

# Crear una nueva actividad
def create_activity_service(db: Session, activity: ActivityCreate):
    # Validar que el título exista
    if not activity.title:
        raise HTTPException(status_code=422, detail="Title is required")        # Error si el título no fue enviado

    # Validar que el título no supere los 30 caracteres
    if len(activity.title) > 30:
        raise HTTPException(status_code=422, detail="Title too long")           # Error si el título es demasiado largo

    # Crear la actividad delegando al repositorio
    return create_activity(db, activity)


# Obtener lista de actividades con paginación
def read_activities_service(db: Session, skip: int = 0, limit: int = 100):
    return read_activities_repo(db, skip=skip, limit=limit)


# Actualizar una actividad existente
def update_activity_service(db: Session, activity_id: int, data: dict):
    # Comprobar si se envió la fecha de la actividad
    if "activity_date" in data:
        activity_date = data["activity_date"]

        # Convertir a datetime si viene como string
        if isinstance(activity_date, str):
            activity_date = datetime.fromisoformat(activity_date)

        # Guardar la fecha convertida
        data["activity_date"] = activity_date

    # Actualizar la actividad en el repositorio
    return update_activity(db, activity_id, data)


# Eliminar una actividad por ID
def delete_activity_service(db: Session, activity_id: int):
    # Eliminar la actividad por ID
    delete_activity(db, activity_id)

    # Respuesta de confirmación
    return {"detail": "Activity deleted successfully"}
