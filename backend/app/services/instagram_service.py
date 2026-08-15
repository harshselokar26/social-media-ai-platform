import httpx
from fastapi import HTTPException


class InstagramService:

    INSTAGRAM_GRAPH_URL = (
        "https://graph.instagram.com/v26.0"
    )

    def __init__(self):
        pass

    # ============================================================
    # INTERNAL REQUEST ERROR HANDLER
    # ============================================================

    @staticmethod
    async def _handle_response(
        response: httpx.Response,
        error_message: str,
    ) -> dict:

        if response.status_code >= 400:

            try:
                meta_response = response.json()
            except Exception:
                meta_response = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": error_message,
                    "meta_response": meta_response,
                },
            )

        return response.json()

    # ============================================================
    # GET INSTAGRAM PROFILE
    # ============================================================

    async def get_profile(
        self,
        instagram_user_id: str,
        access_token: str,
    ) -> dict:

        params = {
            "fields": (
                "id,"
                "username,"
                "name,"
                "profile_picture_url"
            ),
            "access_token": access_token,
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                f"{self.INSTAGRAM_GRAPH_URL}/"
                f"{instagram_user_id}",
                params=params,
            )

        return await self._handle_response(
            response,
            "Failed to fetch Instagram profile",
        )

    # ============================================================
    # GET INSTAGRAM MEDIA
    # ============================================================

    async def get_media(
        self,
        instagram_user_id: str,
        access_token: str,
        limit: int = 25,
    ) -> dict:

        params = {
            "fields": (
                "id,"
                "caption,"
                "media_type,"
                "media_product_type,"
                "media_url,"
                "thumbnail_url,"
                "permalink,"
                "timestamp"
            ),
            "limit": limit,
            "access_token": access_token,
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                f"{self.INSTAGRAM_GRAPH_URL}/"
                f"{instagram_user_id}/media",
                params=params,
            )

        return await self._handle_response(
            response,
            "Failed to fetch Instagram media",
        )

    # ============================================================
    # CREATE IMAGE MEDIA CONTAINER
    # ============================================================

    async def create_image_container(
        self,
        instagram_user_id: str,
        access_token: str,
        image_url: str,
        caption: str | None = None,
        alt_text: str | None = None,
    ) -> dict:

        data = {
            "image_url": image_url,
            "access_token": access_token,
        }

        if caption:
            data["caption"] = caption

        if alt_text:
            data["alt_text"] = alt_text

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.post(
                f"{self.INSTAGRAM_GRAPH_URL}/"
                f"{instagram_user_id}/media",
                data=data,
            )

        return await self._handle_response(
            response,
            "Failed to create Instagram media container",
        )

    # ============================================================
    # CHECK MEDIA CONTAINER STATUS
    # ============================================================

    async def get_container_status(
        self,
        container_id: str,
        access_token: str,
    ) -> dict:

        params = {
            "fields": "status_code,status",
            "access_token": access_token,
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                f"{self.INSTAGRAM_GRAPH_URL}/"
                f"{container_id}",
                params=params,
            )

        return await self._handle_response(
            response,
            "Failed to fetch Instagram container status",
        )

    # ============================================================
    # PUBLISH MEDIA CONTAINER
    # ============================================================

    async def publish_container(
        self,
        instagram_user_id: str,
        access_token: str,
        container_id: str,
    ) -> dict:

        data = {
            "creation_id": container_id,
            "access_token": access_token,
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.post(
                f"{self.INSTAGRAM_GRAPH_URL}/"
                f"{instagram_user_id}/media_publish",
                data=data,
            )

        return await self._handle_response(
            response,
            "Failed to publish Instagram media",
        )

    # ============================================================
    # CREATE + PUBLISH IMAGE
    # ============================================================

    async def publish_image(
        self,
        instagram_user_id: str,
        access_token: str,
        image_url: str,
        caption: str | None = None,
        alt_text: str | None = None,
    ) -> dict:

        # --------------------------------------------------------
        # 1. Create container
        # --------------------------------------------------------

        container = await self.create_image_container(
            instagram_user_id=instagram_user_id,
            access_token=access_token,
            image_url=image_url,
            caption=caption,
            alt_text=alt_text,
        )

        container_id = container.get("id")

        if not container_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Instagram did not return "
                    "a media container ID"
                ),
            )

        # --------------------------------------------------------
        # 2. Publish container
        # --------------------------------------------------------

        published = await self.publish_container(
            instagram_user_id=instagram_user_id,
            access_token=access_token,
            container_id=container_id,
        )

        media_id = published.get("id")

        return {
            "container_id": container_id,
            "media_id": media_id,
            "status": "published",
        }
