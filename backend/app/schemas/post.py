from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    organization_id: UUID | None

    caption: str
    image_url: str
    status: str
    platforms: list[str]

    facebook_post_id: str | None
    instagram_media_id: str | None

    error_message: str | None

    published_at: datetime | None
    scheduled_at: datetime | None

    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    posts: list[PostResponse]
    total: int