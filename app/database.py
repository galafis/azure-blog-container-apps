"""In-memory database for the blog platform.

Provides CRUD operations for all blog models using dictionary-based storage
that simulates a SQLite-like interface.
"""

from datetime import datetime
from typing import Optional

from .models import Post, Category, Tag, Comment


class Database:
    """In-memory database with CRUD operations for blog models.

    Stores all data in dictionaries keyed by entity ID, providing
    fast lookups and simple iteration for filtering.
    """

    def __init__(self) -> None:
        self._posts: dict[str, Post] = {}
        self._categories: dict[str, Category] = {}
        self._tags: dict[str, Tag] = {}
        self._comments: dict[str, Comment] = {}

    # --- Category operations ---

    def create_category(self, name: str, slug: str, description: str = "") -> Category:
        """Create a new category.

        Args:
            name: Category display name.
            slug: URL-friendly identifier.
            description: Optional category description.

        Returns:
            The created Category object.
        """
        category = Category(name=name, slug=slug, description=description)
        self._categories[category.id] = category
        return category

    def get_category(self, category_id: str) -> Optional[Category]:
        """Retrieve a category by its ID."""
        return self._categories.get(category_id)

    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        """Retrieve a category by its slug."""
        for cat in self._categories.values():
            if cat.slug == slug:
                return cat
        return None

    def list_categories(self) -> list[Category]:
        """List all categories."""
        return list(self._categories.values())

    def update_category(self, category_id: str, **kwargs) -> Optional[Category]:
        """Update a category's fields."""
        category = self._categories.get(category_id)
        if not category:
            return None
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        return category

    def delete_category(self, category_id: str) -> bool:
        """Delete a category by ID."""
        if category_id in self._categories:
            del self._categories[category_id]
            return True
        return False

    # --- Tag operations ---

    def create_tag(self, name: str, slug: str) -> Tag:
        """Create a new tag."""
        tag = Tag(name=name, slug=slug)
        self._tags[tag.id] = tag
        return tag

    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Retrieve a tag by its ID."""
        return self._tags.get(tag_id)

    def get_tag_by_slug(self, slug: str) -> Optional[Tag]:
        """Retrieve a tag by its slug."""
        for tag in self._tags.values():
            if tag.slug == slug:
                return tag
        return None

    def list_tags(self) -> list[Tag]:
        """List all tags."""
        return list(self._tags.values())

    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag by ID."""
        if tag_id in self._tags:
            del self._tags[tag_id]
            return True
        return False

    # --- Post operations ---

    def create_post(
        self,
        title: str,
        slug: str,
        content: str,
        author: str,
        category_id: Optional[str] = None,
        tag_ids: Optional[list[str]] = None,
        published: bool = False,
        html_content: str = "",
    ) -> Post:
        """Create a new blog post.

        Args:
            title: Post title.
            slug: URL-friendly identifier.
            content: Markdown content of the post.
            author: Author name.
            category_id: Optional category ID.
            tag_ids: Optional list of tag IDs.
            published: Whether the post should be published immediately.
            html_content: Pre-rendered HTML content.

        Returns:
            The created Post object.
        """
        post = Post(
            title=title,
            slug=slug,
            content=content,
            author=author,
            category_id=category_id,
            tag_ids=tag_ids or [],
            published=published,
            html_content=html_content,
        )
        self._posts[post.id] = post
        return post

    def get_post(self, post_id: str) -> Optional[Post]:
        """Retrieve a post by its ID."""
        return self._posts.get(post_id)

    def get_post_by_slug(self, slug: str) -> Optional[Post]:
        """Retrieve a post by its slug."""
        for post in self._posts.values():
            if post.slug == slug:
                return post
        return None

    def list_posts(
        self,
        published_only: bool = False,
        category_id: Optional[str] = None,
        tag_id: Optional[str] = None,
        author: Optional[str] = None,
    ) -> list[Post]:
        """List posts with optional filtering.

        Args:
            published_only: If True, only return published posts.
            category_id: Filter by category ID.
            tag_id: Filter by tag ID.
            author: Filter by author name.

        Returns:
            List of matching Post objects, sorted by creation date (newest first).
        """
        posts = list(self._posts.values())

        if published_only:
            posts = [p for p in posts if p.published]
        if category_id:
            posts = [p for p in posts if p.category_id == category_id]
        if tag_id:
            posts = [p for p in posts if tag_id in p.tag_ids]
        if author:
            posts = [p for p in posts if p.author == author]

        return sorted(posts, key=lambda p: p.created_at, reverse=True)

    def update_post(self, post_id: str, **kwargs) -> Optional[Post]:
        """Update a post's fields.

        Args:
            post_id: The ID of the post to update.
            **kwargs: Fields to update (e.g., title='New Title').

        Returns:
            The updated Post, or None if not found.
        """
        post = self._posts.get(post_id)
        if not post:
            return None
        for key, value in kwargs.items():
            if hasattr(post, key):
                setattr(post, key, value)
        post.updated_at = datetime.utcnow()
        return post

    def delete_post(self, post_id: str) -> bool:
        """Delete a post and its associated comments."""
        if post_id in self._posts:
            del self._posts[post_id]
            # Also delete associated comments
            comment_ids = [
                cid for cid, c in self._comments.items() if c.post_id == post_id
            ]
            for cid in comment_ids:
                del self._comments[cid]
            return True
        return False

    # --- Comment operations ---

    def create_comment(
        self,
        post_id: str,
        author: str,
        email: str,
        content: str,
        parent_id: Optional[str] = None,
        approved: bool = False,
    ) -> Optional[Comment]:
        """Create a new comment on a post.

        Args:
            post_id: The ID of the post to comment on.
            author: Comment author name.
            email: Comment author email.
            content: Comment text content.
            parent_id: Optional parent comment ID for threaded replies.
            approved: Whether the comment is pre-approved.

        Returns:
            The created Comment, or None if the post doesn't exist.
        """
        if post_id not in self._posts:
            return None

        comment = Comment(
            post_id=post_id,
            author=author,
            email=email,
            content=content,
            parent_id=parent_id,
            approved=approved,
        )
        self._comments[comment.id] = comment
        return comment

    def get_comment(self, comment_id: str) -> Optional[Comment]:
        """Retrieve a comment by its ID."""
        return self._comments.get(comment_id)

    def list_comments(
        self,
        post_id: Optional[str] = None,
        approved_only: bool = False,
    ) -> list[Comment]:
        """List comments with optional filtering.

        Args:
            post_id: Filter by post ID.
            approved_only: If True, only return approved comments.

        Returns:
            List of matching Comment objects sorted by creation date.
        """
        comments = list(self._comments.values())

        if post_id:
            comments = [c for c in comments if c.post_id == post_id]
        if approved_only:
            comments = [c for c in comments if c.approved]

        return sorted(comments, key=lambda c: c.created_at)

    def approve_comment(self, comment_id: str) -> Optional[Comment]:
        """Approve a comment for display."""
        comment = self._comments.get(comment_id)
        if comment:
            comment.approved = True
        return comment

    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment by ID."""
        if comment_id in self._comments:
            del self._comments[comment_id]
            return True
        return False

    # --- Statistics ---

    def get_stats(self) -> dict:
        """Get database statistics."""
        return {
            "total_posts": len(self._posts),
            "published_posts": len([p for p in self._posts.values() if p.published]),
            "draft_posts": len([p for p in self._posts.values() if not p.published]),
            "total_categories": len(self._categories),
            "total_tags": len(self._tags),
            "total_comments": len(self._comments),
            "approved_comments": len(
                [c for c in self._comments.values() if c.approved]
            ),
            "pending_comments": len(
                [c for c in self._comments.values() if not c.approved]
            ),
        }
