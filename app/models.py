"""Data models for the blog platform."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Category:
    """Represents a blog post category.

    Attributes:
        id: Unique identifier for the category.
        name: Category name.
        slug: URL-friendly version of the name.
        description: Optional description of the category.
        created_at: Timestamp when the category was created.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    slug: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class Tag:
    """Represents a tag that can be applied to posts.

    Attributes:
        id: Unique identifier for the tag.
        name: Tag name.
        slug: URL-friendly version of the name.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    slug: str = ""

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "slug": self.slug}


@dataclass
class Post:
    """Represents a blog post.

    Attributes:
        id: Unique identifier for the post.
        title: Post title.
        slug: URL-friendly version of the title.
        content: Post content in markdown format.
        html_content: Rendered HTML content.
        author: Author name.
        category_id: ID of the associated category.
        tag_ids: List of associated tag IDs.
        published: Whether the post is published.
        created_at: Timestamp when the post was created.
        updated_at: Timestamp when the post was last updated.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    slug: str = ""
    content: str = ""
    html_content: str = ""
    author: str = ""
    category_id: Optional[str] = None
    tag_ids: list[str] = field(default_factory=list)
    published: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "html_content": self.html_content,
            "author": self.author,
            "category_id": self.category_id,
            "tag_ids": self.tag_ids,
            "published": self.published,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class Comment:
    """Represents a comment on a blog post.

    Attributes:
        id: Unique identifier for the comment.
        post_id: ID of the post this comment belongs to.
        author: Comment author name.
        email: Comment author email.
        content: Comment text content.
        approved: Whether the comment has been approved for display.
        parent_id: ID of parent comment for threaded replies.
        created_at: Timestamp when the comment was created.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    post_id: str = ""
    author: str = ""
    email: str = ""
    content: str = ""
    approved: bool = False
    parent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "post_id": self.post_id,
            "author": self.author,
            "email": self.email,
            "content": self.content,
            "approved": self.approved,
            "parent_id": self.parent_id,
            "created_at": self.created_at.isoformat(),
        }
