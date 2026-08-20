import uuid

from sqlalchemy import JSON
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )

    caption = Column(
        Text,
        nullable=False,
    )

    image_url = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        index=True,
    )

    platforms = Column(
        JSON,
        nullable=False,
        default=list,
    )

    scheduled_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    facebook_post_id = Column(
        String,
        nullable=True,
    )

    instagram_media_id = Column(
        String,
        nullable=True,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    published_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )