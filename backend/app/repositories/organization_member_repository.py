from sqlalchemy.orm import Session

from app.models.organization_member import (
    OrganizationMember,
    Role,
)


class OrganizationMemberRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        organization_id,
        user_id,
        role: Role = Role.ADMIN,
        commit: bool = True,
    ) -> OrganizationMember:

        membership = OrganizationMember(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        self.db.add(membership)

        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(membership)

        return membership

    def get_by_user_id(self, user_id):
        return (
        self.db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == user_id
        )
        .first()
    )