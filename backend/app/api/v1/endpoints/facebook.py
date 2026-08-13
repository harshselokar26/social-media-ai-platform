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
# Helper
# ---------------------------------------------------------

def get_user_page(
    page_id: str,
    current_user,
    db: Session,
):
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
# GET PAGE
# ---------------------------------------------------------

@router.get("/pages/{page_id}")
async def get_page(
    page_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = get_user_page(page_id, current_user, db)

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
    page = get_user_page(page_id, current_user, db)

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
    page = (
        db.query(FacebookPage)
        .join(
            MetaConnection,
            FacebookPage.meta_connection_id
            == MetaConnection.id,
        )
        .filter(
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

    page_access_token = meta_page.get("access_token")

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
# CREATE TEST POST
# ---------------------------------------------------------

@router.post("/pages/{page_id}/posts")
async def create_post(
    page_id: str,
    message: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = get_user_page(page_id, current_user, db)

    service = FacebookPageService()

    return await service.create_post(
        page.page_id,
        page.page_access_token,
        message,
    )


# ---------------------------------------------------------
# DELETE TEST POST
# ---------------------------------------------------------
async def delete_post(
    self,
    post_id: str,
    page_access_token: str,
):
    params = {
        "access_token": page_access_token,
    }

    try:
        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:


            response = await client.delete(
                f"{self.GRAPH_URL}/{post_id}",
                params=params,
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Meta Graph API timed out while deleting the post",
        )

    if response.status_code != 200:
        try:
            error = response.json()
        except Exception:
            error = response.text

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Failed to delete Facebook post",
                "meta_response": error,
            },
        )

    return response.json()

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = (
        db.query(FacebookPage)
        .join(
            MetaConnection,
            FacebookPage.meta_connection_id
            == MetaConnection.id,
        )
        .filter(
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

    service = FacebookPageService()

    return await service.delete_post(
        post_id,
        page.page_access_token,
    )