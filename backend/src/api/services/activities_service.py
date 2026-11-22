from typing import Any

from sqlalchemy.orm import Session

from src.api.exceptions.activity_exceptions import ActivityNotFound
from src.api.repositories.activities_repo import create_activity, delete_activity, get_activity, update_activity
from src.db.models.activity import Activity
from src.schemas.activity import ActivityCreate


def create_activity_service(db: Session, activity: ActivityCreate) -> Activity:
    return create_activity(db, activity)


def read_activities_service(db: Session, activity_id: int | None) -> Activity | list[Activity]:
    activity = get_activity(db, activity_id)
    if activity is None:
        raise ActivityNotFound()
    return activity


def update_activity_service(db: Session, activity_id: int, data: dict[str, Any]) -> Activity:
    activity = get_activity(db, activity_id)
    if activity is None:
        raise ActivityNotFound()
    return update_activity(db, activity, data)


def delete_activity_service(db: Session, activity_id: int) -> dict[str, str]:
    activity = get_activity(db, activity_id)
    if activity is None:
        raise ActivityNotFound()
    delete_activity(db, activity)
    return {"detail": "Activity deleted successfully"}
