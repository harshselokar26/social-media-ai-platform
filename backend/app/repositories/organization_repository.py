from sqlalchemy.orm import Session

from app.models.organization import Organization


class OrganizationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        name: str,
        slug: str,
        plan: str = "free",
        commit: bool = True,
    ) -> Organization:

        organization = Organization(
            name=name,
            slug=slug,
            plan=plan,
        )

        self.db.add(organization)

        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(organization)

        return organization

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:

        return (
            self.db.query(Organization)
            .filter(Organization.slug == slug)
            .first()
        )

    def get_unique_slug(self, base_slug: str) -> str:
        slug = base_slug
        suffix = 1

        while self.exists(slug):
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        return slug

    def exists(self, slug: str) -> bool:
        return (
            self.db.query(Organization)
            .filter(Organization.slug == slug)
            .first()
            is not None
        )