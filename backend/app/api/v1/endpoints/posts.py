from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.config import settings
from app.db.session import get_db

from app.models.organization_member import OrganizationMember

from app.schemas.publish import PublishPostRequest
from app.schemas.post import PostResponse, PostListResponse
from app.schemas.schedule import SchedulePostRequest

from app.services.publisher_service import PublisherService
from app.services.post_service import PostService
from app.services.scheduler_service import SchedulerService
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
# SCHEDULE POST
# ============================================================

@router.post(
    "/schedule",
    response_model=PostResponse,
)
async def schedule_post(
    request: SchedulePostRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    scheduler = SchedulerService(db)

    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=400,
            detail="User is not a member of any organization.",
        )

    return scheduler.schedule_post(
        user_id=current_user.id,
        organization_id=membership.organization_id,
        caption=request.caption,
        image_url=str(request.image_url),
        platforms=request.platforms,
        scheduled_at=request.scheduled_at,
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

# ============================================================
# GET USER POSTS
# ============================================================

@router.get(
    "",
    response_model=PostListResponse,
)
async def get_posts(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.get_user_posts(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )


# ============================================================
# GET SINGLE POST
# ============================================================

@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
async def get_post(
    post_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.get_user_post(
        user_id=current_user.id,
        post_id=post_id,
    )

# ============================================================
# DELETE POST
# ============================================================

@router.delete("/{post_id}")
async def delete_post(
    post_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.delete_user_post(
        user_id=current_user.id,
        post_id=post_id,
    )