from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from app.core.config import settings


class InstagramAuthService:

    # ============================================================
    # INSTAGRAM OAUTH
    # ============================================================

    INSTAGRAM_OAUTH_URL = (
        "https://www.instagram.com/oauth/authorize"
    )

    INSTAGRAM_TOKEN_URL = (
        "https://api.instagram.com/oauth/access_token"
    )

    # ============================================================
    # INSTAGRAM GRAPH API
    # ============================================================

    INSTAGRAM_GRAPH_URL = (
        "https://graph.instagram.com/v26.0"
    )

    def __init__(self):
        self.app_id = settings.INSTAGRAM_APP_ID
        self.app_secret = settings.INSTAGRAM_APP_SECRET
        self.redirect_uri = settings.INSTAGRAM_REDIRECT_URI

        if not self.app_id:
            raise HTTPException(
                status_code=500,
                detail="INSTAGRAM_APP_ID is not configured",
            )

        if not self.app_secret:
            raise HTTPException(
                status_code=500,
                detail="INSTAGRAM_APP_SECRET is not configured",
            )

        if not self.redirect_uri:
            raise HTTPException(
                status_code=500,
                detail="INSTAGRAM_REDIRECT_URI is not configured",
            )

    # ============================================================
    # GENERATE INSTAGRAM LOGIN URL
    # ============================================================

    def get_login_url(
        self,
        state: str,
    ) -> str:

        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "scope": (
                "instagram_business_basic,"
                "instagram_business_content_publish"
            ),
            "response_type": "code",
            "state": state,
        }

        return (
            f"{self.INSTAGRAM_OAUTH_URL}"
            f"?{urlencode(params)}"
        )

    # ============================================================
    # EXCHANGE AUTHORIZATION CODE
    # FOR SHORT-LIVED ACCESS TOKEN
    # ============================================================

    async def exchange_code_for_token(
        self,
        code: str,
    ) -> dict:

        data = {
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.post(
                self.INSTAGRAM_TOKEN_URL,
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
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
                        "Failed to exchange Instagram "
                        "authorization code"
                    ),
                    "meta_response": meta_response,
                },
            )

        return response.json()

    # ============================================================
    # EXCHANGE SHORT-LIVED TOKEN
    # FOR LONG-LIVED TOKEN
    # ============================================================

    async def exchange_for_long_lived_token(
        self,
        short_lived_token: str,
    ) -> dict:

        params = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.app_secret,
            "access_token": short_lived_token,
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                f"{self.INSTAGRAM_GRAPH_URL}/access_token",
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
                        "Failed to exchange Instagram "
                        "short-lived token"
                    ),
                    "meta_response": meta_response,
                },
            )

        return response.json()

    # ============================================================
    # GET INSTAGRAM ACCOUNT PROFILE
    # ============================================================

    async def get_profile(
        self,
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
                f"{self.INSTAGRAM_GRAPH_URL}/me",
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
                        "Failed to fetch Instagram profile"
                    ),
                    "meta_response": meta_response,
                },
            )

        return response.json()