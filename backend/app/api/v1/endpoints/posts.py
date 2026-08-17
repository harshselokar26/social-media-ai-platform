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
# NORMAL PUBLISH ENDPOINT
# ============================================================

@router.post("/publish")
async def publish_post(
    request: PublishPostRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Publish a post to the selected connected platforms.
    """

    publisher = PublisherService(db)

    return await publisher.publish(
        user_id=current_user.id,
        caption=request.caption,
        image_url=str(request.image_url),
        platforms=request.platforms,
    )


# ============================================================
# FIXED DEVELOPMENT TEST ENDPOINT
# ============================================================

@router.post("/test-publish")
async def test_publish(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Fixed development test endpoint.

    Publishes the same test image and caption
    to Facebook and Instagram.

    No request body is required.
    """

    publisher = PublisherService(db)

    return await publisher.publish(
        user_id=current_user.id,
        caption=settings.TEST_PUBLISH_CAPTION,
        image_url=settings.TEST_PUBLISH_IMAGE_URL,
        platforms=[
            "facebook",
            "instagram",
        ],
    )