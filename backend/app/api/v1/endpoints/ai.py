from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user

from app.schemas.ai import (
    GenerateCaptionRequest,
    GenerateCaptionResponse,
    GenerateImageRequest,
    GenerateImageResponse,
)

from app.services.ai_service import AIService


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/generate-caption",
    response_model=GenerateCaptionResponse,
)
async def generate_caption(
    request: GenerateCaptionRequest,
    current_user=Depends(get_current_user),
):
    try:
        service = AIService()

        result = await service.generate_caption(
            topic=request.topic,
            platform=request.platform,
            tone=request.tone,
        )

        return GenerateCaptionResponse(
            caption=result["caption"],
            hashtags=result["hashtags"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI caption generation failed: {str(exc)}",
        )


@router.post(
    "/generate-image",
    response_model=GenerateImageResponse,
)
async def generate_image(
    request: GenerateImageRequest,
    current_user=Depends(get_current_user),
):
    try:
        service = AIService()

        image_url = await service.generate_image(
            topic=request.topic,
            platform=request.platform,
            aspect_ratio=request.aspect_ratio,
        )

        return GenerateImageResponse(
            image_url=image_url
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI image generation failed: {str(exc)}",
        )