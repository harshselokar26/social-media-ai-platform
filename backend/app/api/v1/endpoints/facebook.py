from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db

from app.models.meta_connection import MetaConnection
from app.models.facebook_page import FacebookPage

from app.services.facebook_page_service import FacebookPageService
from app.services.meta_auth_service import MetaAuthService


router = APIRouter(
    prefix="/facebook",
    tags=["Facebook"],
)


# ---------------------------------------------------------
# HELPER: GET USER PAGE BY PAGE ID
# ---------------------------------------------------------

def get_user_page(
    page_id: str,
    current_user,
    db: Session,
):
    """
    Get an active Facebook Page belonging to the
    currently authenticated user.
    """

    page = (
        db.query(FacebookPage)
        .join(
            MetaConnection,
            FacebookPage.meta_connection_id
            == MetaConnection.id,
        )
        .filter(
            FacebookPage.page_id == page_id,
            MetaConnection.user_id == current_user.id,
            FacebookPage.is_active.is_(True),
        )
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=404,
            detail="Facebook Page not found",
        )

    return page


# ---------------------------------------------------------
# HELPER: GET USER PAGE THAT OWNS A POST
# ---------------------------------------------------------

def get_user_page_for_post(
    post_id: str,
    current_user,
    db: Session,
):
    """
    Resolve the Facebook Page that owns a post.

    Facebook Page post IDs normally have this format:

        PAGE_ID_POST_ID

    Example:

        1174699799071336_122101680675437893

    Page ID:

        1174699799071336
    """

    if "_" not in post_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid Facebook post ID format",
        )

    page_id = post_id.split("_", 1)[0]

    page = get_user_page(
        page_id,
        current_user,
        db,
    )

    return page


# ---------------------------------------------------------
# GET PAGE
# ---------------------------------------------------------

@router.get("/pages/{page_id}")
async def get_page(
    page_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = get_user_page(
        page_id,
        current_user,
        db,
    )

    service = FacebookPageService()

    return await service.get_page(
        page.page_id,
        page.page_access_token,
    )


# ---------------------------------------------------------
# GET POSTS
# ---------------------------------------------------------

@router.get("/pages/{page_id}/posts")
async def get_posts(
    page_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = get_user_page(
        page_id,
        current_user,
        db,
    )

    service = FacebookPageService()

    return await service.get_posts(
        page.page_id,
        page.page_access_token,
    )


# ---------------------------------------------------------
# GET COMMENTS
# ---------------------------------------------------------

@router.get("/posts/{post_id}/comments")
async def get_comments(
    post_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get comments for a Facebook post.

    The Page is resolved from the post ID so that the
    correct Page access token is used.
    """

    page = get_user_page_for_post(
        post_id,
        current_user,
        db,
    )

    service = FacebookPageService()

    return await service.get_comments(
        post_id,
        page.page_access_token,
    )


# ---------------------------------------------------------
# GET PAGE INSIGHTS
# ---------------------------------------------------------

@router.get("/pages/{page_id}/insights")
async def get_page_insights(
    page_id: str,
    metric: str = "page_views_total",
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(MetaConnection)
        .filter(
            MetaConnection.user_id == current_user.id
        )
        .first()
    )

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Meta account is not connected",
        )

    service = MetaAuthService()

    pages = await service.get_pages(
        connection.access_token
    )

    meta_page = next(
        (
            p
            for p in pages.get("data", [])
            if p.get("id") == page_id
        ),
        None,
    )

    if not meta_page:
        raise HTTPException(
            status_code=404,
            detail="Facebook Page not found",
        )

    page_access_token = meta_page.get(
        "access_token"
    )

    if not page_access_token:
        raise HTTPException(
            status_code=400,
            detail="Page access token was not returned by Meta",
        )

    return await service.get_page_insights(
        page_id=page_id,
        page_access_token=page_access_token,
        metric=metric,
    )


# ---------------------------------------------------------
# CREATE POST
# ---------------------------------------------------------

@router.post("/pages/{page_id}/posts")
async def create_post(
    page_id: str,
    message: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a Facebook Page post.

    Page ID is explicitly provided in the URL, so the
    correct Page access token is used.
    """

    page = get_user_page(
        page_id,
        current_user,
        db,
    )

    service = FacebookPageService()

    return await service.create_post(
        page.page_id,
        page.page_access_token,
        message,
    )

# ---------------------------------------------------------
# CREATE IMAGE POST
# ---------------------------------------------------------

@router.post("/pages/{page_id}/image-posts")
async def create_image_post(
    page_id: str,
    image_url: str,
    message: str | None = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create an image post on a Facebook Page.
    """

    page = get_user_page(
        page_id,
        current_user,
        db,
    )

    service = FacebookPageService()

    return await service.create_image_post(
        page_id=page.page_id,
        page_access_token=page.page_access_token,
        image_url=image_url,
        message=message,
    )


# ---------------------------------------------------------
# DELETE POST
# ---------------------------------------------------------

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a Facebook post.

    The Page is resolved from the post ID so that the
    correct Page access token is used.
    """

    page = get_user_page_for_post(
        post_id,
        current_user,
        db,
    )

    service = FacebookPageService()

    return await service.delete_post(
        post_id,
        page.page_access_token,
    )