from realtime import Any
from sqlalchemy.orm import Session
from models.activity import Activity, ActivityCreate

# Función para obtener actividad o actividades
def get_activity(db: Session, activity_id: int | None) -> Activity | list[Activity]:
    if not activity_id:
        return db.query(Activity).all()
    return db.query(Activity).filter(Activity.id == activity_id).first()

# Crea una nueva fila en la tabla activities
def create_activity(db: Session, activity_data: ActivityCreate) -> Activity:
    data_dict = activity_data.model_dump()          # Convierte el Pydantic model a dict
    new_activity = Activity(**data_dict)            # Crear la instancia de Activity con ** unpacking
    db.add(new_activity)                            # Agregar a la sesión de la DB
    db.commit()                                     # db.commit() guarda cambios
    db.refresh(new_activity)                        # db.refresh() actualiza el objeto con los datos finales de la DB
    return new_activity

# Actualiza la fila por id
def update_activity(db: Session, activity: Activity, data: dict[str, Any]) -> Activity:
    # Actualización dinámica de campos
    for key, value in data.items():
        setattr(activity, key, value)

    db.commit()                    # db.commit() guarda cambios
    db.refresh(activity)           # db.refresh() actualiza el objeto con los datos finales de la DB
    return activity


# Elimina la fila por id
def delete_activity(db: Session, activity: Activity) -> bool:  
    db.delete(activity)      # Eliminarla
    db.commit()              # Confirmar cambios en la DB
    return True