from fastapi.responses import RedirectResponse
from app.models.meta_connection import MetaConnection
from app.models.facebook_page import FacebookPage
from app.models.instagram_account import InstagramAccount
from app.services.instagram_service import InstagramService
from app.schemas.instagram import InstagramPublishRequest

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.db.session import get_db

from app.exceptions.auth import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)

from app.schemas.auth import RegisterRequest
from app.schemas.user import UserResponse

from app.services.auth_service import AuthService
from app.services.meta_auth_service import MetaAuthService
from app.services.meta_state_service import MetaStateService
from app.services.instagram_auth_service import InstagramAuthService
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)





# ============================================================
# REGISTER
# ============================================================

@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.register(request)

    except EmailAlreadyExistsException:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.login(
            form_data.username,
            form_data.password,
        )

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user=Depends(get_current_user),
):
    return current_user


# ============================================================
# ADMIN TEST
# ============================================================

@router.get("/admin-test")
def admin_test(
    current_user=Depends(require_admin),
):
    return {
        "message": "admin access granted",
        "user": current_user.name,
    }


# ============================================================
# META LOGIN
# ============================================================

@router.get("/meta")
def meta_login(
    current_user=Depends(get_current_user),
):
    """
    Start Meta OAuth login.
    """

    # Create secure OAuth state
    state_service = MetaStateService()

    state = state_service.create_state(
        current_user.id
    )

    # Create Meta authentication service
    service = MetaAuthService()

    # Generate Meta OAuth URL
    login_url = service.get_login_url(
        state
    )

    # Return the OAuth URL instead of redirecting.
    # This makes the endpoint testable from Swagger UI.
    # Open the returned auth_url in a normal browser tab to continue
    # the Meta OAuth flow. The existing callback remains unchanged.
    return {
        "auth_url": login_url
    }


# ============================================================
# META CALLBACK
# ============================================================

@router.get("/meta/callback")
async def meta_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    """
    Meta OAuth callback.

    Flow:
        1. Verify OAuth state
        2. Exchange authorization code for access token
        3. Fetch Meta user
        4. Save/update Meta connection
    """

    # --------------------------------------------------------
    # 1. Verify OAuth state
    # --------------------------------------------------------

    state_service = MetaStateService()

    try:
        user_id = state_service.verify_state(
            state
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state",
        )

    # --------------------------------------------------------
    # 2. Create Meta service
    # --------------------------------------------------------

    service = MetaAuthService()

    # --------------------------------------------------------
    # 3. Exchange authorization code for access token
    # --------------------------------------------------------

    token_data = await service.exchange_code_for_token(
        code
    )

    access_token = token_data.get(
        "access_token"
    )

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Meta access token was not returned",
        )

    # --------------------------------------------------------
    # 4. Get Meta user
    # --------------------------------------------------------

    meta_user = await service.get_meta_user(
        access_token
    )

    meta_user_id = meta_user.get("id")
    meta_name = meta_user.get("name")

    if not meta_user_id:
        raise HTTPException(
            status_code=400,
            detail="Meta user ID was not returned",
        )

    # --------------------------------------------------------
    # 5. Find existing Meta connection
    # --------------------------------------------------------

    connection = (
        db.query(MetaConnection)
        .filter(
            MetaConnection.user_id == user_id
        )
        .first()
    )

    # --------------------------------------------------------
    # 6. Update existing connection
    # --------------------------------------------------------

    if connection:

        connection.meta_user_id = meta_user_id
        connection.meta_name = meta_name
        connection.access_token = access_token
        connection.token_type = token_data.get(
            "token_type"
        )
        connection.expires_in = token_data.get(
            "expires_in"
        )

    # --------------------------------------------------------
    # 7. Create new connection
    # --------------------------------------------------------

    else:

        connection = MetaConnection(
            user_id=user_id,
            meta_user_id=meta_user_id,
            meta_name=meta_name,
            access_token=access_token,
            token_type=token_data.get(
                "token_type"
            ),
            expires_in=token_data.get(
                "expires_in"
            ),
        )

        db.add(connection)

    # --------------------------------------------------------
    # 8. Save database changes
    # --------------------------------------------------------

    db.commit()
    db.refresh(connection)

    # Never return the access token to the browser

    return {
        "message": "Meta account connected successfully",
        "meta_user_id": meta_user_id,
        "meta_name": meta_name,
    }


# ============================================================
# GET FACEBOOK PAGES
# ============================================================

@router.get("/meta/pages")
async def meta_pages(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Fetch Facebook Pages associated with the
    connected Meta account.

    Page access tokens are stored server-side
    and are never returned to the client.
    """

    # --------------------------------------------------------
    # 1. Find Meta connection
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 2. Create Meta service
    # --------------------------------------------------------

    service = MetaAuthService()

    # --------------------------------------------------------
    # 3. Fetch Facebook Pages from Meta
    # --------------------------------------------------------

    pages_response = await service.get_pages(
        connection.access_token
    )

    pages = pages_response.get(
        "data",
        []
    )

    # --------------------------------------------------------
    # 4. Save/update each Facebook Page
    # --------------------------------------------------------

    response_pages = []

    for page in pages:

        page_id = page.get("id")
        page_name = page.get("name")
        page_access_token = page.get("access_token")

        if not page_id or not page_name:
            continue

        # ----------------------------------------------------
        # Find existing Page
        # ----------------------------------------------------

        facebook_page = (
            db.query(FacebookPage)
            .filter(
                FacebookPage.page_id == page_id
            )
            .first()
        )

        # ----------------------------------------------------
        # Update existing Page
        # ----------------------------------------------------

        if facebook_page:

            facebook_page.page_name = page_name

            if page_access_token:
                facebook_page.page_access_token = (
                    page_access_token
                )

            facebook_page.meta_connection_id = (
                connection.id
            )

            facebook_page.is_active = True

        # ----------------------------------------------------
        # Create new Page
        # ----------------------------------------------------

        else:

            if not page_access_token:
                continue

            facebook_page = FacebookPage(
                meta_connection_id=connection.id,
                page_id=page_id,
                page_name=page_name,
                page_access_token=page_access_token,
                is_active=True,
            )

            db.add(facebook_page)

        # ----------------------------------------------------
        # Safe response
        # ----------------------------------------------------

        response_pages.append(
            {
                "id": page_id,
                "name": page_name,
            }
        )

    # --------------------------------------------------------
    # 5. Save database changes
    # --------------------------------------------------------

    db.commit()

    # --------------------------------------------------------
    # 6. Return ONLY safe Page information
    # --------------------------------------------------------

    return RedirectResponse(
    url="https://social-media-ai-frotend.onrender.com/accounts",
    status_code=302,
)

# ============================================================
# INSTAGRAM LOGIN
# ============================================================

@router.get("/instagram")
def instagram_login(
    current_user=Depends(get_current_user),
):
    """
    Start Instagram OAuth login.
    """

    # Reuse the existing secure OAuth state mechanism.
    state_service = MetaStateService()

    state = state_service.create_state(
        current_user.id
    )

    service = InstagramAuthService()

    login_url = service.get_login_url(
        state
    )

    return {
        "auth_url": login_url
    }


# ============================================================
# INSTAGRAM CALLBACK
# ============================================================

@router.get("/instagram/callback")
async def instagram_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    """
    Instagram OAuth callback.

    Flow:
        1. Verify OAuth state
        2. Exchange authorization code
        3. Exchange for long-lived token
        4. Fetch Instagram profile
        5. Save/update Instagram account
    """

    # --------------------------------------------------------
    # 1. Verify OAuth state
    # --------------------------------------------------------

    state_service = MetaStateService()

    try:
        user_id = state_service.verify_state(
            state
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state",
        )

    # --------------------------------------------------------
    # 2. Create Instagram service
    # --------------------------------------------------------

    service = InstagramAuthService()

    # --------------------------------------------------------
    # 3. Exchange authorization code
    # --------------------------------------------------------

    token_data = await service.exchange_code_for_token(
        code
    )

    short_lived_token = token_data.get(
        "access_token"
    )

    if not short_lived_token:
        raise HTTPException(
            status_code=400,
            detail=(
                "Instagram access token was not returned"
            ),
        )

    # --------------------------------------------------------
    # 4. Exchange for long-lived token
    # --------------------------------------------------------

    long_lived_token_data = (
        await service.exchange_for_long_lived_token(
            short_lived_token
        )
    )

    access_token = long_lived_token_data.get(
        "access_token"
    )

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail=(
                "Long-lived Instagram access token "
                "was not returned"
            ),
        )

    # --------------------------------------------------------
    # 5. Get Instagram profile
    # --------------------------------------------------------

    instagram_profile = await service.get_profile(
        access_token
    )

    instagram_user_id = (
        instagram_profile.get("id")
        or instagram_profile.get("user_id")
    )

    username = instagram_profile.get(
        "username"
    )

    name = instagram_profile.get(
        "name"
    )

    if not instagram_user_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Instagram user ID was not returned"
            ),
        )

    # --------------------------------------------------------
    # 6. Find existing Instagram account
    # --------------------------------------------------------

    instagram_account = (
        db.query(InstagramAccount)
        .filter(
            InstagramAccount.instagram_user_id
            == instagram_user_id
        )
        .first()
    )

    # --------------------------------------------------------
    # 7. Update existing account
    # --------------------------------------------------------

    if instagram_account:

        # Make sure the Instagram account belongs
        # to the authenticated application user.

        user_connections = (
            db.query(MetaConnection)
            .filter(
                MetaConnection.user_id == user_id
            )
            .all()
        )

        user_connection_ids = {
            connection.id
            for connection in user_connections
        }

        if (
            instagram_account.meta_connection_id
            not in user_connection_ids
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Instagram account belongs to "
                    "another user"
                ),
            )

        instagram_account.username = username
        instagram_account.name = name
        instagram_account.access_token = access_token
        instagram_account.is_active = True

    # --------------------------------------------------------
    # 8. Create new Instagram account
    # --------------------------------------------------------

    else:

        connection = (
            db.query(MetaConnection)
            .filter(
                MetaConnection.user_id == user_id
            )
            .first()
        )

        if not connection:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Meta connection not found. "
                    "Connect your Meta account first."
                ),
            )

        instagram_account = InstagramAccount(
            meta_connection_id=connection.id,
            instagram_user_id=instagram_user_id,
            username=username,
            name=name,
            access_token=access_token,
            is_active=True,
        )

        db.add(instagram_account)

    # --------------------------------------------------------
    # 9. Save database changes
    # --------------------------------------------------------

    db.commit()
    db.refresh(instagram_account)

    # --------------------------------------------------------
    # 10. Never return access token
    # --------------------------------------------------------

    return RedirectResponse(
    url="https://social-media-ai-frotend.onrender.com/accounts",
    status_code=302,
)

# ============================================================
# GET CONNECTED INSTAGRAM ACCOUNT
# ============================================================

@router.get("/instagram/account")
async def get_instagram_account(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get the currently connected Instagram account.
    """

    instagram_account = (
        db.query(InstagramAccount)
        .join(
            MetaConnection,
            InstagramAccount.meta_connection_id
            == MetaConnection.id,
        )
        .filter(
            MetaConnection.user_id == current_user.id,
            InstagramAccount.is_active.is_(True),
        )
        .first()
    )

    if not instagram_account:
        raise HTTPException(
            status_code=404,
            detail="No Instagram account connected",
        )

    service = InstagramService()

    profile = await service.get_profile(
        instagram_user_id=(
            instagram_account.instagram_user_id
        ),
        access_token=(
            instagram_account.access_token
        ),
    )

    return {
        "id": profile.get("id"),
        "username": profile.get("username"),
        "name": profile.get("name"),
        "profile_picture_url": profile.get(
            "profile_picture_url"
        ),
    }

# ============================================================
# GET INSTAGRAM MEDIA
# ============================================================

@router.get("/instagram/media")
async def get_instagram_media(
    limit: int = 25,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get media from the connected Instagram account.
    """

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100",
        )

    instagram_account = (
        db.query(InstagramAccount)
        .join(
            MetaConnection,
            InstagramAccount.meta_connection_id
            == MetaConnection.id,
        )
        .filter(
            MetaConnection.user_id == current_user.id,
            InstagramAccount.is_active.is_(True),
        )
        .first()
    )

    if not instagram_account:
        raise HTTPException(
            status_code=404,
            detail="No Instagram account connected",
        )

    service = InstagramService()

    media = await service.get_media(
        instagram_user_id=(
            instagram_account.instagram_user_id
        ),
        access_token=(
            instagram_account.access_token
        ),
        limit=limit,
    )

    return media

# ============================================================
# PUBLISH INSTAGRAM IMAGE
# ============================================================

@router.post("/instagram/publish")
async def publish_instagram_image(
    request: InstagramPublishRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Publish an image to the connected Instagram account.

    Flow:
        1. Find connected Instagram account
        2. Get server-side access token
        3. Create Instagram media container
        4. Publish the container
        5. Return publishing result
    """

    # --------------------------------------------------------
    # 1. Find connected Instagram account
    # --------------------------------------------------------

    instagram_account = (
        db.query(InstagramAccount)
        .join(
            MetaConnection,
            InstagramAccount.meta_connection_id
            == MetaConnection.id,
        )
        .filter(
            MetaConnection.user_id == current_user.id,
            InstagramAccount.is_active.is_(True),
        )
        .first()
    )

    if not instagram_account:
        raise HTTPException(
            status_code=404,
            detail="No Instagram account connected",
        )

    # --------------------------------------------------------
    # 2. Create Instagram service
    # --------------------------------------------------------

    service = InstagramService()

    # --------------------------------------------------------
    # 3. Publish image
    # --------------------------------------------------------

    result = await service.publish_image(
        instagram_user_id=(
            instagram_account.instagram_user_id
        ),
        access_token=(
            instagram_account.access_token
        ),
        image_url=str(request.image_url),
        caption=request.caption,
        alt_text=request.alt_text,
    )

    # --------------------------------------------------------
    # 4. Safe response
    # --------------------------------------------------------

    return {
        "message": "Instagram post published successfully",
        "instagram_user_id": (
            instagram_account.instagram_user_id
        ),
        "container_id": result.get(
            "container_id"
        ),
        "media_id": result.get(
            "media_id"
        ),
        "status": result.get(
            "status"
        ),
    }