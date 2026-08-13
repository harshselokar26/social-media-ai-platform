from itsdangerous import URLSafeTimedSerializer

from app.core.config import settings


class MetaStateService:

    def __init__(self):
        self.serializer = URLSafeTimedSerializer(
            settings.JWT_SECRET
        )

    def create_state(
        self,
        user_id,
    ) -> str:

        return self.serializer.dumps(
            {
                "user_id": str(user_id)
            }
        )

    def verify_state(
        self,
        state: str,
        max_age: int = 600,
    ):

        try:

            data = self.serializer.loads(
                state,
                max_age=max_age,
            )

            return data["user_id"]

        except Exception:

            raise ValueError(
                "Invalid or expired OAuth state"
            )