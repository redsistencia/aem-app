from typing import Any
from sqlalchemy.orm import Session
from models.activity import Activity, ActivityCreate
from datetime import datetime
from exceptions.activity_exceptions import ActivityNotFound, ActivityErrorDateFormat, ActivityTitleRequired, ActivityTitleTooLong
from repositories.activities_repo import (
    get_activity,
    delete_activity,
    update_activity,
    create_activity
)

# Crear una nueva actividad
def create_activity_service(db: Session, activity: ActivityCreate) -> Activity:
    # Validar que el título exista
    if not activity.title:
        raise ActivityTitleRequired()        # Error si el título no fue enviado
    # Validar que el título no supere los 30 caracteres
    if len(activity.title) > 30:
        raise ActivityTitleTooLong()           # Error si el título es demasiado largo
    
    # Crear la actividad delegando al repositorio
    return create_activity(db, activity)


# Obtener una actividad por ID o todas las actividades
def read_activities_service(db: Session, activity_id: int | None) -> Activity | list[Activity]:
    act = get_activity(db, activity_id)
    if not act:
        raise ActivityNotFound()
    return act


# Actualizar una actividad existente
def update_activity_service(db: Session, activity_id: int, data: dict[str, Any]) -> Activity:
    # Obtener la actividad existente
    activity = get_activity(db, activity_id)
    if not activity:
        raise ActivityNotFound()
    # Comprobar si se envió la fecha de la actividad
    if "activity_date" in data:
        # Convertir a datetime si viene como string
        activity_date = data["activity_date"]
        if isinstance(activity_date, str):
            try:
                activity_date = datetime.fromisoformat(activity_date)
            except ValueError:
                raise ActivityErrorDateFormat()
        # Guardar la fecha convertida
        data["activity_date"] = activity_date
    # Actualizar la actividad en el repositorio
    return update_activity(db, activity, data)


# Eliminar una actividad por ID
def delete_activity_service(db: Session, activity_id: int) -> dict[str, str]:
    # Verificar si la actividad existe
    activity = get_activity(db, activity_id)
    if not activity:
        raise ActivityNotFound()
    # Eliminar la actividad por ID
    delete_activity(db, activity)

    # Respuesta de confirmación
    return {"detail": "Activity deleted successfully"}
