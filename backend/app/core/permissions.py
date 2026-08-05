from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models.organization_member import Role
from app.models.user import User


def require_role(*allowed_roles: Role):
    def _dependency(current_user: User = Depends(get_current_user)) -> User:
        for membership in getattr(current_user, "memberships", []):
            role = membership.role
            if role in allowed_roles:
                return current_user

        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return _dependency


require_admin = require_role(Role.ADMIN)
require_manager = require_role(Role.MANAGER)
require_editor = require_role(Role.EDITOR)
require_viewer = require_role(Role.VIEWER)
