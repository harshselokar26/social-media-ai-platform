from typing import Literal

from pydantic import BaseModel, HttpUrl


class PublishPostRequest(BaseModel):
    caption: str
    image_url: HttpUrl
    platforms: list[Literal["facebook", "instagram"]]