import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class InstagramAccount(Base):
    __tablename__ = "instagram_accounts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    meta_connection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meta_connections.id"),
        nullable=False,
        index=True,
    )

    instagram_user_id = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    username = Column(
        String,
        nullable=True,
    )

    name = Column(
        String,
        nullable=True,
    )

    access_token = Column(
        Text,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )