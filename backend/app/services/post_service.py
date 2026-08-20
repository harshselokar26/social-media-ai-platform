from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.post import Post


class PostService:

    def __init__(self, db: Session):
        self.db = db

    def get_user_posts(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ):
        query = (
            self.db.query(Post)
            .filter(Post.user_id == user_id)
            .order_by(Post.created_at.desc())
        )

        total = query.count()

        posts = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "posts": posts,
            "total": total,
        }

    def get_user_post(
        self,
        user_id: UUID,
        post_id: UUID,
    ):
        post = (
            self.db.query(Post)
            .filter(
                Post.id == post_id,
                Post.user_id == user_id,
            )
            .first()
        )

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        return post

    def delete_user_post(
        self,
        user_id: UUID,
        post_id: UUID,
    ):
        post = (
            self.db.query(Post)
            .filter(
                Post.id == post_id,
                Post.user_id == user_id,
            )
            .first()
        )

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        self.db.delete(post)
        self.db.commit()

        return {
            "message": "Post deleted successfully",
            "post_id": str(post_id),
        }
    