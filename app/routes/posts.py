"""Post API endpoint handlers.

Provides a Flask-like interface for managing blog posts through
simple function-based endpoints that operate on the database.
"""

from typing import Optional
from ..database import Database
from ..services.markdown_renderer import MarkdownRenderer


class PostRouter:
    """Handles post-related API operations.

    Provides CRUD methods that simulate REST API endpoint handlers.
    Each method returns a dictionary response similar to a JSON API response.
    """

    def __init__(self, db: Database) -> None:
        self.db = db
        self.renderer = MarkdownRenderer()

    def create_post(
        self,
        title: str,
        content: str,
        author: str,
        category_id: Optional[str] = None,
        tag_ids: Optional[list[str]] = None,
        published: bool = False,
    ) -> dict:
        """Create a new blog post.

        Args:
            title: Post title.
            content: Markdown content.
            author: Author name.
            category_id: Optional category ID.
            tag_ids: Optional list of tag IDs.
            published: Whether to publish immediately.

        Returns:
            Response dictionary with status and post data.
        """
        slug = self._generate_slug(title)
        html_content = self.renderer.render(content)

        post = self.db.create_post(
            title=title,
            slug=slug,
            content=content,
            html_content=html_content,
            author=author,
            category_id=category_id,
            tag_ids=tag_ids,
            published=published,
        )

        return {"status": 201, "message": "Post created", "data": post.to_dict()}

    def get_post(self, post_id: str) -> dict:
        """Retrieve a post by ID.

        Args:
            post_id: The post identifier.

        Returns:
            Response dictionary with status and post data, or 404 error.
        """
        post = self.db.get_post(post_id)
        if not post:
            return {"status": 404, "message": "Post not found"}
        return {"status": 200, "data": post.to_dict()}

    def get_post_by_slug(self, slug: str) -> dict:
        """Retrieve a post by its URL slug.

        Args:
            slug: The URL-friendly post identifier.

        Returns:
            Response dictionary with status and post data, or 404 error.
        """
        post = self.db.get_post_by_slug(slug)
        if not post:
            return {"status": 404, "message": "Post not found"}
        return {"status": 200, "data": post.to_dict()}

    def list_posts(
        self,
        published_only: bool = False,
        category_id: Optional[str] = None,
        tag_id: Optional[str] = None,
        author: Optional[str] = None,
    ) -> dict:
        """List posts with optional filtering.

        Returns:
            Response dictionary with status and list of post data.
        """
        posts = self.db.list_posts(
            published_only=published_only,
            category_id=category_id,
            tag_id=tag_id,
            author=author,
        )
        return {
            "status": 200,
            "data": [p.to_dict() for p in posts],
            "count": len(posts),
        }

    def update_post(self, post_id: str, **kwargs) -> dict:
        """Update a post's fields.

        If content is updated, the HTML is re-rendered.

        Args:
            post_id: The post identifier.
            **kwargs: Fields to update.

        Returns:
            Response dictionary with status and updated post data.
        """
        if "content" in kwargs:
            kwargs["html_content"] = self.renderer.render(kwargs["content"])

        if "title" in kwargs:
            kwargs["slug"] = self._generate_slug(kwargs["title"])

        post = self.db.update_post(post_id, **kwargs)
        if not post:
            return {"status": 404, "message": "Post not found"}
        return {"status": 200, "message": "Post updated", "data": post.to_dict()}

    def delete_post(self, post_id: str) -> dict:
        """Delete a post and its associated comments.

        Args:
            post_id: The post identifier.

        Returns:
            Response dictionary with status.
        """
        success = self.db.delete_post(post_id)
        if not success:
            return {"status": 404, "message": "Post not found"}
        return {"status": 200, "message": "Post deleted"}

    def publish_post(self, post_id: str) -> dict:
        """Publish a draft post.

        Args:
            post_id: The post identifier.

        Returns:
            Response dictionary with status.
        """
        post = self.db.update_post(post_id, published=True)
        if not post:
            return {"status": 404, "message": "Post not found"}
        return {"status": 200, "message": "Post published", "data": post.to_dict()}

    def unpublish_post(self, post_id: str) -> dict:
        """Unpublish a post (revert to draft).

        Args:
            post_id: The post identifier.

        Returns:
            Response dictionary with status.
        """
        post = self.db.update_post(post_id, published=False)
        if not post:
            return {"status": 404, "message": "Post not found"}
        return {"status": 200, "message": "Post unpublished", "data": post.to_dict()}

    @staticmethod
    def _generate_slug(title: str) -> str:
        """Generate a URL-friendly slug from a title.

        Args:
            title: The post title.

        Returns:
            A lowercase, hyphenated slug string.
        """
        slug = title.lower().strip()
        # Replace spaces and special chars with hyphens
        result = []
        for char in slug:
            if char.isalnum():
                result.append(char)
            elif char in (" ", "_", "-"):
                result.append("-")
        slug = "".join(result)
        # Remove consecutive hyphens
        while "--" in slug:
            slug = slug.replace("--", "-")
        return slug.strip("-")
