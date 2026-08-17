from pydantic import BaseModel, HttpUrl


class InstagramPublishRequest(BaseModel):
    image_url: HttpUrl
    caption: str | None = None
    alt_text: str | None = None