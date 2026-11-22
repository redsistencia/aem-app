from datetime import date, datetime

from sqlalchemy import String, Date, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(450))
    date: Mapped[date] = mapped_column(Date)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    # Conservamos los datos del esquema anterior al agregar fecha y slug.
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activity_date: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, server_default=func.now())
