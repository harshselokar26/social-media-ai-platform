from typing import Literal

from pydantic import BaseModel, Field


class GenerateCaptionRequest(BaseModel):
    topic: str = Field(
        min_length=2,
        max_length=500,
    )

    platform: Literal[
        "facebook",
        "instagram",
    ] = "instagram"

    tone: Literal[
        "professional",
        "casual",
        "friendly",
        "promotional",
        "funny",
    ] = "professional"


class GenerateCaptionResponse(BaseModel):
    caption: str
    hashtags: list[str]


class GenerateImageRequest(BaseModel):
    topic: str = Field(
        min_length=2,
        max_length=500,
    )

    platform: Literal[
        "facebook",
        "instagram",
    ] = "instagram"

    aspect_ratio: Literal[
        "1:1",
        "4:5",
        "9:16",
        "16:9",
    ] = "4:5"


class GenerateImageResponse(BaseModel):
    image_url: str