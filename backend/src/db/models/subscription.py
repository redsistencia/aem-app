from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    privacy_policy: Mapped[bool] = mapped_column(Boolean, nullable=False)
    newsletter_consent: Mapped[bool] = mapped_column(Boolean, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
