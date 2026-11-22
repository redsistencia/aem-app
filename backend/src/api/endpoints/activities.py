from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.security.auth import require_role
from src.api.services.activities_service import (
    create_activity_service, read_activities_service, delete_activity_service, update_activity_service,
)
from src.db.models.activity import Activity
from src.db.session import get_db
from src.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate

router = APIRouter(prefix="/admin/activities", tags=["Admin · Activities"])
public_router = APIRouter(prefix="/activities", tags=["Activities"])


@public_router.get("/", response_model=list[ActivityRead])
def list_public_activities(db: Session = Depends(get_db)):
    return db.query(Activity).order_by(Activity.date.desc(), Activity.id.desc()).all()


@public_router.get("/{slug}", response_model=ActivityRead)
def get_public_activity(slug: str, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.slug == slug).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/", response_model=list[ActivityRead], dependencies=[Depends(require_role("admin", "editor"))])
def get_all_activities(db: Session = Depends(get_db)):
    return read_activities_service(db, None)


@router.get("/{activity_id}", response_model=ActivityRead, dependencies=[Depends(require_role("admin", "editor"))])
def get_activity_endpoint(activity_id: int, db: Session = Depends(get_db)):
    return read_activities_service(db, activity_id)


@router.post("/", response_model=ActivityRead, status_code=201, dependencies=[Depends(require_role("admin"))])
def create_activity_endpoint(activity_data: ActivityCreate, db: Session = Depends(get_db)):
    return create_activity_service(db, activity_data)


@router.patch("/{activity_id}", response_model=ActivityRead, dependencies=[Depends(require_role("admin", "editor"))])
def update_activity_endpoint(activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db)):
    return update_activity_service(db, activity_id, activity_data.model_dump(exclude_unset=True))


@router.delete("/{activity_id}", dependencies=[Depends(require_role("admin", "editor"))])
def delete_activity_endpoint(activity_id: int, db: Session = Depends(get_db)):
    return delete_activity_service(db, activity_id)
