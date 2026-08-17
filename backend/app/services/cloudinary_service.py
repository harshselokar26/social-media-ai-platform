import cloudinary
import cloudinary.uploader

from fastapi import HTTPException

from app.core.config import settings


class CloudinaryService:

    def __init__(self):

        if not settings.CLOUDINARY_NAME:
            raise HTTPException(
                status_code=500,
                detail="CLOUDINARY_NAME is not configured",
            )

        if not settings.CLOUDINARY_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="CLOUDINARY_API_KEY is not configured",
            )

        if not settings.CLOUDINARY_API_SECRET:
            raise HTTPException(
                status_code=500,
                detail="CLOUDINARY_API_SECRET is not configured",
            )

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

    # ============================================================
    # UPLOAD IMAGE
    # ============================================================

    async def upload_image(
        self,
        file,
        folder: str = "social-media-platform",
    ) -> dict:

        try:

            result = cloudinary.uploader.upload(
                file,
                resource_type="image",
                folder=folder,
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Failed to upload image to Cloudinary",
                    "error": str(exc),
                },
            )

        return {
            "public_id": result.get("public_id"),
            "secure_url": result.get("secure_url"),
            "format": result.get("format"),
            "width": result.get("width"),
            "height": result.get("height"),
            "resource_type": result.get("resource_type"),
        }