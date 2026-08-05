from slugify import slugify

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.exceptions.auth import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)

from app.repositories.user_repository import UserRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.organization_member_repository import (
    OrganizationMemberRepository,
)

from app.models.organization_member import Role


class AuthService:

    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.org_repo = OrganizationRepository(db)
        self.member_repo = OrganizationMemberRepository(db)

    # 👇 STEP 5 GOES HERE
    def register(self, data):
        if self.user_repo.exists(data.email):
            raise EmailAlreadyExistsException()

        base_slug = slugify(data.organization_name)
        slug = self.org_repo.get_unique_slug(base_slug)

        db = self.user_repo.db

        try:
            organization = self.org_repo.create(
                name=data.organization_name,
                slug=slug,
                commit=False,
            )

            user = self.user_repo.create(
                name=data.name,
                email=data.email,
                password_hash=hash_password(data.password),
                commit=False,
            )

            membership = self.member_repo.create(
                organization_id=organization.id,
                user_id=user.id,
                role=Role.ADMIN,
                commit=False,
            )

            db.commit()

            db.refresh(organization)
            db.refresh(user)
            db.refresh(membership)

        except Exception:
            db.rollback()
            raise

        return {
            "access_token": create_access_token(
                subject=str(user.id),
                organization_id=str(organization.id),
                role=membership.role.value,
            ),
            "token_type": "bearer",
        }

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    # 👇 STEP 6 GOES HERE
    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        membership = self.member_repo.get_by_user_id(user.id)

        token = create_access_token(
            subject=str(user.id),
            organization_id=str(membership.organization_id),
            role=membership.role.value,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }