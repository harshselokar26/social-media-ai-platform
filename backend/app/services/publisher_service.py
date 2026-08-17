from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings

from app.models.meta_connection import MetaConnection
from app.models.facebook_page import FacebookPage
from app.models.instagram_account import InstagramAccount

from app.services.facebook_page_service import FacebookPageService
from app.services.instagram_service import InstagramService


class PublisherService:

    def __init__(self, db: Session):
        self.db = db

        self.facebook_service = FacebookPageService()
        self.instagram_service = InstagramService()

    async def publish(
        self,
        user_id,
        caption: str,
        image_url: str,
        platforms: list[str],
        facebook_page_id: str | None = None,
    ):

        results = {}

        # ========================================================
        # FACEBOOK
        # ========================================================

        if "facebook" in platforms:

            # ----------------------------------------------------
            # TEMPORARY DEVELOPMENT BEHAVIOR
            #
            # If no page_id is supplied, use the fixed test page.
            # Later we will replace this with real account/page
            # selection from the frontend.
            # ----------------------------------------------------

            selected_page_id = (
                facebook_page_id
                or settings.FACEBOOK_TEST_PAGE_ID
            )

            if not selected_page_id:
                results["facebook"] = {
                    "status": "failed",
                    "message": (
                        "FACEBOOK_TEST_PAGE_ID is not configured"
                    ),
                }

            else:

                facebook_page = (
                    self.db.query(FacebookPage)
                    .join(
                        MetaConnection,
                        FacebookPage.meta_connection_id
                        == MetaConnection.id,
                    )
                    .filter(
                        MetaConnection.user_id == user_id,
                        FacebookPage.page_id
                        == selected_page_id,
                        FacebookPage.is_active.is_(True),
                    )
                    .first()
                )

                print(
                    "========== FACEBOOK PUBLISH DEBUG =========="
                )
                print("USER ID:", user_id)
                print(
                    "REQUESTED PAGE ID:",
                    facebook_page_id,
                )
                print(
                    "SELECTED PAGE ID:",
                    selected_page_id,
                )
                print(
                    "DB PAGE FOUND:",
                    bool(facebook_page),
                )
                print(
                    "TOKEN EXISTS:",
                    bool(
                        facebook_page.page_access_token
                    )
                    if facebook_page
                    else False,
                )
                print(
                    "============================================"
                )

                if not facebook_page:

                    results["facebook"] = {
                        "status": "failed",
                        "message": (
                            "Configured Facebook test Page "
                            "is not connected to this user"
                        ),
                        "page_id": selected_page_id,
                    }

                else:

                    try:

                        response = (
                            await self.facebook_service
                            .create_image_post(
                                page_id=facebook_page.page_id,
                                page_access_token=(
                                    facebook_page.page_access_token
                                ),
                                image_url=image_url,
                                message=caption,
                            )
                        )

                        results["facebook"] = {
                            "status": "published",
                            "page_id": facebook_page.page_id,
                            "post_id": response.get(
                                "post_id"
                            ),
                            "response": response,
                        }

                    except HTTPException as exc:

                        results["facebook"] = {
                            "status": "failed",
                            "message": exc.detail,
                            "page_id": facebook_page.page_id,
                        }

        # ========================================================
        # INSTAGRAM
        # ========================================================

        if "instagram" in platforms:

            instagram_account = (
                self.db.query(InstagramAccount)
                .join(
                    MetaConnection,
                    InstagramAccount.meta_connection_id
                    == MetaConnection.id,
                )
                .filter(
                    MetaConnection.user_id == user_id,
                    InstagramAccount.is_active.is_(True),
                )
                .first()
            )

            if not instagram_account:

                results["instagram"] = {
                    "status": "failed",
                    "message": (
                        "No active Instagram account connected"
                    ),
                }

            else:

                try:

                    response = (
                        await self.instagram_service
                        .publish_image(
                            instagram_user_id=(
                                instagram_account
                                .instagram_user_id
                            ),
                            access_token=(
                                instagram_account.access_token
                            ),
                            image_url=image_url,
                            caption=caption,
                        )
                    )

                    results["instagram"] = {
                        "status": "published",
                        "account": (
                            instagram_account.username
                        ),
                        "media_id": response.get(
                            "media_id"
                        ),
                        "response": response,
                    }

                except HTTPException as exc:

                    results["instagram"] = {
                        "status": "failed",
                        "message": exc.detail,
                    }

        # ========================================================
        # FINAL STATUS
        # ========================================================

        statuses = [
            result["status"]
            for result in results.values()
        ]

        if statuses and all(
            status == "published"
            for status in statuses
        ):
            overall_status = "published"

        elif any(
            status == "published"
            for status in statuses
        ):
            overall_status = "partial"

        else:
            overall_status = "failed"

        return {
            "status": overall_status,
            "results": results,
        }