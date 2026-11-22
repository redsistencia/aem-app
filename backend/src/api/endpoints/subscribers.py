from datetime import datetime, timezone
from hmac import compare_digest

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.models.subscriber import SubscriberCreate, SubscriberRead, SubscriberUpdate, UnsubscribeRequest
from src.api.security.auth import require_role
from src.api.services.subscribers_service import (
    create_subscriber_service, update_subscriber_service, get_subscriber_service, delete_subscriber_service,
)
from src.api.repositories.subscribers_repo import get_subscriber, update_subscriber
from src.db.session import get_db

router = APIRouter(prefix="/admin/subscribers", tags=["Admin · Asociades"])
public_router = APIRouter(prefix="/subscribers", tags=["Asociades"])


@router.get("/", response_model=list[SubscriberRead], dependencies=[Depends(require_role("admin"))])
def get_all_subscribers(db: Session = Depends(get_db)):
    return get_subscriber_service(db, None)


@router.get("/{entry}", response_model=SubscriberRead, dependencies=[Depends(require_role("admin"))])
def get_subscriber_endpoint(entry: str, db: Session = Depends(get_db)):
    return get_subscriber_service(db, entry)


@public_router.post("/", response_model=SubscriberRead, status_code=201)
@router.post("/", response_model=SubscriberRead, status_code=201)
def create_subscriber_endpoint(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    return create_subscriber_service(db, subscriber)


@public_router.post("/unsubscribe")
def unsubscribe(data: UnsubscribeRequest, db: Session = Depends(get_db)):
    subscriber = get_subscriber(db, data.email)
    if subscriber is None or not subscriber.document_id or not compare_digest(
        subscriber.document_id.strip().casefold().encode(), data.document_id.casefold().encode()
    ):
        raise HTTPException(status_code=400, detail="No se pudieron verificar los datos de la baja")
    if subscriber.active or subscriber.newsletter:
        update_subscriber(db, subscriber, {
            "active": False,
            "newsletter": False,
            "termination_date": datetime.now(timezone.utc),
        })
    return {"success": True}


@router.patch("/{subscriber_id}", response_model=SubscriberRead, dependencies=[Depends(require_role("admin"))])
def update_subscriber_endpoint(subscriber_id: int, subscriber_data: SubscriberUpdate, db: Session = Depends(get_db)):
    return update_subscriber_service(db, subscriber_id, subscriber_data.model_dump(exclude_unset=True))


@router.delete("/{entry}", dependencies=[Depends(require_role("admin"))])
def delete_subscriber_endpoint(entry: str, db: Session = Depends(get_db)):
    return delete_subscriber_service(db, entry)
