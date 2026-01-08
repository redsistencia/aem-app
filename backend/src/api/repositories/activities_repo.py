from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.activity import Activity, ActivityCreate

# Crea una nueva fila en la tabla activities
def create_activity(db: Session, activity_data: ActivityCreate):
    data_dict = activity_data.dict()        # Convierte el Pydantic model a dict
    new_activity = Activity(**data_dict)    # Crear la instancia de Activity con ** unpacking
    db.add(new_activity)                    # Agregar a la sesión de la DB
    db.commit()                             # db.commit() guarda cambios
    db.refresh(new_activity)                # db.refresh() actualiza el objeto con los datos finales de la DB
    return new_activity


# Funcion para leer actividades con paginación
#       skip: Numero de filas a saltar en caso de paginación.
#       limit: Limite de filtas a mostrar.
def read_activities(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(Activity).offset(skip).limit(limit).all()   # Consulta con paginación

# Busca la fila por id
def update_activity(db: Session, activity_id: int, data: dict):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()    # Buscar la actividad por id
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")       # Si no existe, lanzar error 404
    
    # Convertir activity_date si viene como string
    if "activity_date" in data and isinstance(data["activity_date"], str):
        try:
            data["activity_date"] = datetime.fromisoformat(data["activity_date"])
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format. Use ISO format.")
        
    # Actualización dinámica de campos
    for key, value in data.items():
        setattr(activity, key, value)

    db.commit()                    # db.commit() guarda cambios
    db.refresh(activity)           # db.refresh() actualiza el objeto con los datos finales de la DB
    return activity


# Elimina la fila por id
def delete_activity(db: Session, activity_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()    # Buscar la actividad por id
    
    # Si no existe, lanzar error 404
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)      # Si existe, eliminarla
    db.commit()              # Confirmar cambios en la DB
    return True