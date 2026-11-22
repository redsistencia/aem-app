from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.exceptions.base import AppException
from src.db.models.activity import Activity
from src.schemas.activity import ActivityCreate


def get_activity(db: Session, activity_id: int | None) -> Activity | list[Activity] | None:
    if activity_id is None:
        return db.query(Activity).order_by(Activity.date.desc(), Activity.id.desc()).all()
    return db.query(Activity).filter(Activity.id == activity_id).first()


def save_activity(db: Session, activity: Activity) -> Activity:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppException("An activity with this slug already exists", 409)
    db.refresh(activity)
    return activity


def create_activity(db: Session, activity_data: ActivityCreate) -> Activity:
    activity = Activity(**activity_data.model_dump())
    db.add(activity)
    return save_activity(db, activity)


def update_activity(db: Session, activity: Activity, data: dict[str, Any]) -> Activity:
    for key, value in data.items():
        setattr(activity, key, value)
    return save_activity(db, activity)


def delete_activity(db: Session, activity: Activity) -> bool:
    db.delete(activity)
    db.commit()
    return True
