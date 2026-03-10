"""Demo script for the Blog Container Apps platform.

Demonstrates creating posts, categories, tags, and comments
using the in-memory blog database and API routes.
"""

from app.database import Database
from app.routes.posts import PostRouter
from app.routes.comments import CommentRouter
from app.services.markdown_renderer import MarkdownRenderer


def print_separator() -> None:
    """Print a visual separator line."""
    print("=" * 60)


def demo_markdown_rendering() -> None:
    """Demonstrate markdown to HTML rendering."""
    print_separator()
    print("MARKDOWN RENDERING DEMO")
    print_separator()

    renderer = MarkdownRenderer()

    sample_md = """# Welcome to the Blog

This is a **bold** statement and this is *italic*.

## Features

- Simple markdown rendering
- Support for code blocks
- Link and image support

Here is some `inline code` and a [link](https://example.com).

```python
def hello():
    print("Hello, World!")
```

> This is a blockquote with important information.
"""

    html = renderer.render(sample_md)
    print(f"Markdown input ({len(sample_md)} chars):")
    print(sample_md[:200] + "...")
    print(f"\nHTML output ({len(html)} chars):")
    print(html[:300] + "...")
    print()


def demo_blog_operations() -> None:
    """Demonstrate full blog CRUD operations."""
    print_separator()
    print("BLOG OPERATIONS DEMO")
    print_separator()

    # Initialize database and routers
    db = Database()
    posts = PostRouter(db)
    comments = CommentRouter(db)

    # Create categories
    tech_cat = db.create_category(
        name="Technology", slug="technology", description="Tech articles"
    )
    travel_cat = db.create_category(
        name="Travel", slug="travel", description="Travel stories"
    )
    print(f"\nCategories created: {tech_cat.name}, {travel_cat.name}")

    # Create tags
    python_tag = db.create_tag(name="Python", slug="python")
    azure_tag = db.create_tag(name="Azure", slug="azure")
    docker_tag = db.create_tag(name="Docker", slug="docker")
    print(f"Tags created: {python_tag.name}, {azure_tag.name}, {docker_tag.name}")

    # Create posts
    post1_response = posts.create_post(
        title="Getting Started with Azure Container Apps",
        content="# Azure Container Apps\n\nLearn how to deploy your **first** container app.",
        author="Gabriel Lafis",
        category_id=tech_cat.id,
        tag_ids=[azure_tag.id, docker_tag.id],
        published=True,
    )
    print(f"\nPost 1 created: {post1_response['data']['title']}")
    print(f"  Slug: {post1_response['data']['slug']}")
    print(f"  Status: {'Published' if post1_response['data']['published'] else 'Draft'}")

    post2_response = posts.create_post(
        title="Python Best Practices for 2025",
        content="## Python Tips\n\n- Use type hints\n- Write tests\n- Document your code",
        author="Gabriel Lafis",
        category_id=tech_cat.id,
        tag_ids=[python_tag.id],
        published=False,
    )
    print(f"\nPost 2 created: {post2_response['data']['title']}")
    print(f"  Status: {'Published' if post2_response['data']['published'] else 'Draft'}")

    # Publish post 2
    publish_response = posts.publish_post(post2_response["data"]["id"])
    print(f"  Published: {publish_response['message']}")

    # Add comments
    post1_id = post1_response["data"]["id"]

    comment1 = comments.create_comment(
        post_id=post1_id,
        author="Maria",
        email="maria@example.com",
        content="Great article! Very helpful for beginners.",
    )
    print(f"\nComment added by {comment1['data']['author']}")

    comment2 = comments.create_comment(
        post_id=post1_id,
        author="Joao",
        email="joao@example.com",
        content="Can you write more about scaling?",
    )
    print(f"Comment added by {comment2['data']['author']}")

    # Reply to comment
    reply = comments.create_comment(
        post_id=post1_id,
        author="Gabriel Lafis",
        email="gabriel@example.com",
        content="Sure! I will cover scaling in the next post.",
        parent_id=comment2["data"]["id"],
    )
    print(f"Reply added by {reply['data']['author']}")

    # Approve comments
    comments.approve_comment(comment1["data"]["id"])
    comments.approve_comment(comment2["data"]["id"])
    comments.approve_comment(reply["data"]["id"])
    print("\nAll comments approved.")

    # List published posts
    all_posts = posts.list_posts(published_only=True)
    print(f"\nPublished posts: {all_posts['count']}")
    for p in all_posts["data"]:
        print(f"  - {p['title']} by {p['author']}")

    # List approved comments
    post_comments = comments.list_comments(post_id=post1_id, approved_only=True)
    print(f"\nApproved comments on post 1: {post_comments['count']}")
    for c in post_comments["data"]:
        prefix = "  Reply:" if c["parent_id"] else "  Comment:"
        print(f"{prefix} {c['author']}: {c['content'][:50]}")

    # Database stats
    stats = db.get_stats()
    print(f"\nDatabase Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()


def main() -> None:
    """Run all demo functions."""
    print("\n  BLOG CONTAINER APPS PLATFORM")
    print("  Plataforma de Blog com Container Apps\n")

    demo_markdown_rendering()
    demo_blog_operations()

    print_separator()
    print("Demo complete / Demo concluida")
    print_separator()


if __name__ == "__main__":
    main()
