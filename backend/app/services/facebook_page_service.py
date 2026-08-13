import httpx
from fastapi import HTTPException


class FacebookPageService:

    GRAPH_URL = "https://graph.facebook.com/v26.0"

    # ---------------------------------------------------------
    # GET PAGE
    # ---------------------------------------------------------

    async def get_page(
        self,
        page_id: str,
        page_access_token: str,
    ):
        params = {
            "fields": "id,name,about,category,fan_count",
            "access_token": page_access_token,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.GRAPH_URL}/{page_id}",
                params=params,
            )

        if response.status_code != 200:
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to fetch Facebook Page",
                    "meta_response": error,
                },
            )

        return response.json()

    # ---------------------------------------------------------
    # GET POSTS
    # ---------------------------------------------------------

    async def get_posts(
        self,
        page_id: str,
        page_access_token: str,
    ):
        params = {
            "fields": "id,message,created_time",
            "access_token": page_access_token,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.GRAPH_URL}/{page_id}/posts",
                params=params,
            )

        if response.status_code != 200:
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to fetch Facebook posts",
                    "meta_response": error,
                },
            )

        return response.json()

    # ---------------------------------------------------------
    # GET COMMENTS
    # ---------------------------------------------------------

    async def get_comments(
        self,
        post_id: str,
        page_access_token: str,
    ):
        params = {
            "fields": "id,message,from,created_time",
            "access_token": page_access_token,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.GRAPH_URL}/{post_id}/comments",
                params=params,
            )

        if response.status_code != 200:
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to fetch Facebook comments",
                    "meta_response": error,
                },
            )

        return response.json()

    # ---------------------------------------------------------
    # CREATE POST
    # ---------------------------------------------------------

    async def create_post(
        self,
        page_id: str,
        page_access_token: str,
        message: str,
    ):
        data = {
            "message": message,
            "access_token": page_access_token,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.GRAPH_URL}/{page_id}/feed",
                data=data,
            )

        if response.status_code not in (200, 201):
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to create Facebook Page post",
                    "meta_response": error,
                },
            )

        return response.json()

    # ---------------------------------------------------------
    # DELETE POST
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
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(
                    f"{self.GRAPH_URL}/{post_id}",
                    params=params,
                )

        except httpx.ReadTimeout:
            raise HTTPException(
                status_code=504,
                detail={
                    "message": "Facebook timed out while processing the delete request",
                    "post_id": post_id,
                },
            )

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "Facebook request failed",
                    "error": str(e),
                },
            )

        if response.status_code != 200:
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise HTTPException(
                status_code=response.status_code,
                detail={
                    "message": "Failed to delete Facebook post",
                    "meta_response": error,
                },
            )

        return response.json()