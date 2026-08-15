from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from app.core.config import settings


class MetaAuthService:

    META_OAUTH_URL = (
        "https://www.facebook.com/v26.0/dialog/oauth"
    )

    META_TOKEN_URL = (
        "https://graph.facebook.com/v26.0/oauth/access_token"
    )

    META_ME_URL = (
        "https://graph.facebook.com/v26.0/me"
    )

    META_ME_ACCOUNTS_URL = (
        "https://graph.facebook.com/v26.0/me/accounts"
    )

    META_PAGE_INSIGHTS_URL = (
        "https://graph.facebook.com/v26.0/{page_id}/insights"
    )

    def __init__(self):
        self.app_id = settings.META_APP_ID
        self.app_secret = settings.META_APP_SECRET
        self.redirect_uri = settings.META_REDIRECT_URI

        if not self.app_id:
            raise HTTPException(
                status_code=500,
                detail="META_APP_ID is not configured",
            )

        if not self.app_secret:
            raise HTTPException(
                status_code=500,
                detail="META_APP_SECRET is not configured",
            )

        if not self.redirect_uri:
            raise HTTPException(
                status_code=500,
                detail="META_REDIRECT_URI is not configured",
            )

    # ============================================================
    # META LOGIN URL
    # ============================================================

    def get_login_url(
        self,
        state: str,
    ) -> str:

        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "scope": (
                "public_profile,"
                "pages_show_list,"
                "pages_read_engagement,"
                "pages_manage_posts,"
                "pages_manage_metadata,"
                "pages_read_user_content,"
                "pages_manage_engagement",
            ),
            "response_type": "code",
            "state": state,
        }

        return (
            f"{self.META_OAUTH_URL}?{urlencode(params)}"
        )

    # ============================================================
    # EXCHANGE AUTHORIZATION CODE FOR ACCESS TOKEN
    # ============================================================

    async def exchange_code_for_token(
        self,
        code: str,
    ):

        params = {
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.META_TOKEN_URL,
                params=params,
            )

        if response.status_code != 200:

            try:
                meta_response = response.json()
            except Exception:
                meta_response = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": (
                        "Failed to exchange Meta authorization code"
                    ),
                    "meta_response": meta_response,
                },
            )

        return response.json()

    # ============================================================
    # GET META USER
    # ============================================================

    async def get_meta_user(
        self,
        access_token: str,
    ):

        params = {
            "fields": "id,name",
            "access_token": access_token,
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.META_ME_URL,
                params=params,
            )

        if response.status_code != 200:

            try:
                meta_response = response.json()
            except Exception:
                meta_response = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to fetch Meta user",
                    "meta_response": meta_response,
                },
            )

        return response.json()

    # ============================================================
    # GET FACEBOOK PAGES
    # ============================================================

    async def get_pages(
        self,
        access_token: str,
    ):

        params = {
            "fields": "id,name,access_token",
            "access_token": access_token,
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.META_ME_ACCOUNTS_URL,
                params=params,
            )

        if response.status_code != 200:

            try:
                meta_response = response.json()
            except Exception:
                meta_response = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to fetch Facebook Pages",
                    "meta_response": meta_response,
                },
            )

        return response.json()

    # ============================================================
    # GET FACEBOOK PAGE INSIGHTS
    # ============================================================

    async def get_page_insights(
        self,
        page_id: str,
        page_access_token: str,
        metric: str = "page_views_total",
    ):

        params = {
            "metric": metric,
            "access_token": page_access_token,
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.META_PAGE_INSIGHTS_URL.format(
                    page_id=page_id
                ),
                params=params,
            )

        if response.status_code != 200:

            try:
                meta_response = response.json()
            except Exception:
                meta_response = response.text

            raise HTTPException(
                status_code=400,
                detail={
                    "message": (
                        "Failed to fetch Facebook Page insights"
                    ),
                    "meta_response": meta_response,
                },
            )

        return response.json()