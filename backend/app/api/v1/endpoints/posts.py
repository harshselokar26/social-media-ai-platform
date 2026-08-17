from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.config import settings
from app.db.session import get_db

from app.schemas.publish import PublishPostRequest
from app.services.publisher_service import PublisherService


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# ============================================================
# ORIGINAL UNIFIED PUBLISH ENDPOINT
# ============================================================

@router.post("/publish")
async def publish_post(
    request: PublishPostRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    print("========== UNIFIED PUBLISH DEBUG ==========")
    print("USER ID:", current_user.id)
    print("CAPTION:", request.caption)
    print("IMAGE URL:", request.image_url)
    print("PLATFORMS:", request.platforms)
    print("===========================================")

    publisher = PublisherService(db)

    return await publisher.publish(
        user_id=current_user.id,
        caption=request.caption,
        image_url=str(request.image_url),
        platforms=request.platforms,
    )


# ============================================================
# FIXED DEVELOPMENT TEST
# ============================================================

@router.post("/test-publish")
async def test_publish(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    publisher = PublisherService(db)

    return await publisher.publish(
        user_id=current_user.id,
        caption=settings.TEST_PUBLISH_CAPTION,
        image_url=settings.TEST_PUBLISH_IMAGE_URL,
        platforms=[
            "facebook",
            "instagram",
        ],
        facebook_page_id=settings.FACEBOOK_TEST_PAGE_ID,
    )