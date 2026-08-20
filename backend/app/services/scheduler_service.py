from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.post import Post
from app.services.publisher_service import PublisherService


class SchedulerService:

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE SCHEDULED POST
    # ============================================================

    def schedule_post(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
        caption: str,
        image_url: str,
        platforms: list[str],
        scheduled_at: datetime,
    ) -> Post:

        # Make sure the scheduled time is timezone-aware.
        if scheduled_at.tzinfo is None:
            raise ValueError(
                "scheduled_at must include timezone information."
            )

        # Don't allow scheduling in the past.
        if scheduled_at <= datetime.now(timezone.utc):
            raise ValueError(
                "scheduled_at must be in the future."
            )

        post = Post(
            user_id=user_id,
            organization_id=organization_id,
            caption=caption,
            image_url=image_url,
            platforms=platforms,
            status="scheduled",
            scheduled_at=scheduled_at,
        )

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        print(
            f"Scheduled post created: {post.id} "
            f"for {post.scheduled_at}"
        )

        return post

    # ============================================================
    # PROCESS DUE POSTS
    # ============================================================

    async def process_scheduled_posts(self):

        now = datetime.now(timezone.utc)

        posts = (
            self.db.query(Post)
            .filter(
                Post.status == "scheduled",
                Post.scheduled_at.isnot(None),
                Post.scheduled_at <= now,
            )
            .order_by(Post.scheduled_at.asc())
            .limit(10)
            .all()
        )

        if not posts:
            return 0

        publisher = PublisherService(self.db)

        processed = 0

        for post in posts:

            try:

                print(
                    f"Processing scheduled post: {post.id}"
                )

                # Prevent another scheduler cycle from
                # picking this post up again.
                post.status = "publishing"

                self.db.commit()

                result = await publisher.publish(
                    user_id=post.user_id,
                    caption=post.caption,
                    image_url=post.image_url,
                    platforms=post.platforms,
                )

                overall_status = result.get("status")

                post.status = overall_status

                facebook_result = (
                    result
                    .get("results", {})
                    .get("facebook")
                )

                instagram_result = (
                    result
                    .get("results", {})
                    .get("instagram")
                )

                if facebook_result:
                    post.facebook_post_id = (
                        facebook_result.get("post_id")
                    )

                if instagram_result:
                    post.instagram_media_id = (
                        instagram_result.get("media_id")
                    )

                if overall_status == "published":

                    post.published_at = datetime.now(
                        timezone.utc
                    )

                    post.error_message = None

                elif overall_status in (
                    "failed",
                    "partial",
                ):

                    post.error_message = str(result)

                self.db.commit()

                processed += 1

                print(
                    f"Scheduled post {post.id} "
                    f"completed with status: "
                    f"{overall_status}"
                )

            except Exception as exc:

                self.db.rollback()

                print(
                    f"Scheduled post {post.id} failed: {exc}"
                )

                failed_post = (
                    self.db.query(Post)
                    .filter(Post.id == post.id)
                    .first()
                )

                if failed_post:

                    failed_post.status = "failed"
                    failed_post.error_message = str(exc)

                    self.db.commit()

                processed += 1

        return processed