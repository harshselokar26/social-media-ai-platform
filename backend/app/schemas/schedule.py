from datetime import datetime
from typing import Literal

from pydantic import BaseModel, HttpUrl, field_validator


class SchedulePostRequest(BaseModel):
    caption: str
    image_url: HttpUrl
    platforms: list[Literal["facebook", "instagram"]]
    scheduled_at: datetime

    @field_validator("caption")
    @classmethod
    def validate_caption(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Caption cannot be empty.")

        return value

    @field_validator("platforms")
    @classmethod
    def validate_platforms(cls, value):
        if not value:
            raise ValueError(
                "At least one platform must be selected."
            )

        return list(dict.fromkeys(value))