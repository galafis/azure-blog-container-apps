"""Comment API endpoint handlers.

Provides a Flask-like interface for managing blog post comments
through simple function-based endpoints.
"""

from typing import Optional
from ..database import Database


class CommentRouter:
    """Handles comment-related API operations.

    Provides CRUD methods that simulate REST API endpoint handlers.
    """

    def __init__(self, db: Database) -> None:
        self.db = db

    def create_comment(
        self,
        post_id: str,
        author: str,
        email: str,
        content: str,
        parent_id: Optional[str] = None,
    ) -> dict:
        """Create a new comment on a post.

        Args:
            post_id: The post to comment on.
            author: Comment author name.
            email: Comment author email.
            content: Comment text.
            parent_id: Optional parent comment for threading.

        Returns:
            Response dictionary with status and comment data.
        """
        comment = self.db.create_comment(
            post_id=post_id,
            author=author,
            email=email,
            content=content,
            parent_id=parent_id,
        )

        if not comment:
            return {"status": 404, "message": "Post not found"}

        return {
            "status": 201,
            "message": "Comment created",
            "data": comment.to_dict(),
        }

    def get_comment(self, comment_id: str) -> dict:
        """Retrieve a comment by ID.

        Args:
            comment_id: The comment identifier.

        Returns:
            Response dictionary with status and comment data, or 404 error.
        """
        comment = self.db.get_comment(comment_id)
        if not comment:
            return {"status": 404, "message": "Comment not found"}
        return {"status": 200, "data": comment.to_dict()}

    def list_comments(
        self,
        post_id: Optional[str] = None,
        approved_only: bool = False,
    ) -> dict:
        """List comments with optional filtering.

        Args:
            post_id: Filter by post ID.
            approved_only: If True, only show approved comments.

        Returns:
            Response dictionary with status and list of comments.
        """
        comments = self.db.list_comments(
            post_id=post_id, approved_only=approved_only
        )
        return {
            "status": 200,
            "data": [c.to_dict() for c in comments],
            "count": len(comments),
        }

    def approve_comment(self, comment_id: str) -> dict:
        """Approve a comment for public display.

        Args:
            comment_id: The comment identifier.

        Returns:
            Response dictionary with status.
        """
        comment = self.db.approve_comment(comment_id)
        if not comment:
            return {"status": 404, "message": "Comment not found"}
        return {
            "status": 200,
            "message": "Comment approved",
            "data": comment.to_dict(),
        }

    def delete_comment(self, comment_id: str) -> dict:
        """Delete a comment.

        Args:
            comment_id: The comment identifier.

        Returns:
            Response dictionary with status.
        """
        success = self.db.delete_comment(comment_id)
        if not success:
            return {"status": 404, "message": "Comment not found"}
        return {"status": 200, "message": "Comment deleted"}

    def get_comment_thread(self, post_id: str, parent_id: Optional[str] = None) -> dict:
        """Get a threaded view of comments for a post.

        Args:
            post_id: The post ID to get comments for.
            parent_id: If provided, only get replies to this comment.

        Returns:
            Response dictionary with threaded comment data.
        """
        all_comments = self.db.list_comments(post_id=post_id, approved_only=True)

        if parent_id:
            thread = [c for c in all_comments if c.parent_id == parent_id]
        else:
            thread = [c for c in all_comments if c.parent_id is None]

        return {
            "status": 200,
            "data": [c.to_dict() for c in thread],
            "count": len(thread),
        }
