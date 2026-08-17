from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from app.services.cloudinary_service import CloudinaryService
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    """
    Upload an image to Cloudinary.
    """

    if not file.content_type:
        return {
            "message": "Invalid file type"
        }

    if not file.content_type.startswith("image/"):
        return {
            "message": "Only image files are supported"
        }

    contents = await file.read()

    service = CloudinaryService()

    result = await service.upload_image(
        file=contents,
        folder="social-media-platform",
    )

    return {
        "message": "Image uploaded successfully",
        "data": result,
    }