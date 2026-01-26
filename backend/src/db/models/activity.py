from sqlalchemy import String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(450))
    date: Mapped[str] = mapped_column(Date)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
