from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Organization(BaseModel):

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    plan: Mapped[str] = mapped_column(
        String(20),
        default="free",
    )

    members = relationship(
        "OrganizationMember",
        back_populates="organization",
        cascade="all, delete",
    )