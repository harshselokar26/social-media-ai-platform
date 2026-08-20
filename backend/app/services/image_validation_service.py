from io import BytesIO

import httpx
from PIL import Image


class ImageValidationService:

    MIN_ASPECT_RATIO = 0.8
    MAX_ASPECT_RATIO = 1.91

    async def validate_instagram_image(
        self,
        image_url: str,
    ) -> dict:

        try:
            async with httpx.AsyncClient(
                timeout=20.0,
                follow_redirects=True,
            ) as client:

                response = await client.get(image_url)

                response.raise_for_status()

        except httpx.HTTPError as exc:
            raise ValueError(
                f"Unable to download image: {exc}"
            )

        try:
            image = Image.open(
                BytesIO(response.content)
            )

            width, height = image.size

        except Exception:
            raise ValueError(
                "The uploaded URL is not a valid image."
            )

        if width <= 0 or height <= 0:
            raise ValueError(
                "Invalid image dimensions."
            )

        aspect_ratio = width / height

        if not (
            self.MIN_ASPECT_RATIO
            <= aspect_ratio
            <= self.MAX_ASPECT_RATIO
        ):
            raise ValueError(
                "Instagram image aspect ratio must be "
                "between 0.8 (4:5) and 1.91:1. "
                f"Received {width}x{height} "
                f"(aspect ratio {aspect_ratio:.2f})."
            )

        return {
            "valid": True,
            "width": width,
            "height": height,
            "aspect_ratio": round(
                aspect_ratio,
                4,
            ),
            "format": image.format,
        }