"""Tests for the blog platform - models, database, routes, and markdown rendering."""

import unittest

from app.models import Post, Category, Tag, Comment
from app.database import Database
from app.routes.posts import PostRouter
from app.routes.comments import CommentRouter
from app.services.markdown_renderer import MarkdownRenderer


class TestModels(unittest.TestCase):
    """Test data model creation and serialization."""

    def test_post_creation(self):
        post = Post(title="Test Post", content="Content", author="Author")
        self.assertEqual(post.title, "Test Post")
        self.assertFalse(post.published)

    def test_post_to_dict(self):
        post = Post(title="Test", author="A")
        d = post.to_dict()
        self.assertIn("title", d)
        self.assertIn("id", d)
        self.assertIn("created_at", d)

    def test_category_creation(self):
        cat = Category(name="Tech", slug="tech")
        self.assertEqual(cat.name, "Tech")

    def test_tag_creation(self):
        tag = Tag(name="Python", slug="python")
        self.assertEqual(tag.slug, "python")

    def test_comment_creation(self):
        comment = Comment(post_id="123", author="User", content="Nice!")
        self.assertFalse(comment.approved)
        self.assertIsNone(comment.parent_id)

    def test_comment_to_dict(self):
        comment = Comment(post_id="abc", author="X", content="Y")
        d = comment.to_dict()
        self.assertEqual(d["post_id"], "abc")


class TestDatabase(unittest.TestCase):
    """Test database CRUD operations."""

    def setUp(self):
        self.db = Database()

    def test_create_category(self):
        cat = self.db.create_category("Tech", "tech")
        self.assertEqual(cat.name, "Tech")
        self.assertIsNotNone(self.db.get_category(cat.id))

    def test_get_category_by_slug(self):
        self.db.create_category("Tech", "tech")
        cat = self.db.get_category_by_slug("tech")
        self.assertIsNotNone(cat)
        self.assertEqual(cat.name, "Tech")

    def test_list_categories(self):
        self.db.create_category("A", "a")
        self.db.create_category("B", "b")
        self.assertEqual(len(self.db.list_categories()), 2)

    def test_delete_category(self):
        cat = self.db.create_category("Del", "del")
        self.assertTrue(self.db.delete_category(cat.id))
        self.assertIsNone(self.db.get_category(cat.id))

    def test_delete_nonexistent_category(self):
        self.assertFalse(self.db.delete_category("nonexistent"))

    def test_create_tag(self):
        tag = self.db.create_tag("Python", "python")
        self.assertEqual(tag.name, "Python")

    def test_create_post(self):
        post = self.db.create_post("Title", "slug", "Content", "Author")
        self.assertEqual(post.title, "Title")
        self.assertFalse(post.published)

    def test_get_post_by_slug(self):
        self.db.create_post("Title", "test-slug", "Content", "Author")
        post = self.db.get_post_by_slug("test-slug")
        self.assertIsNotNone(post)

    def test_list_posts_published_only(self):
        self.db.create_post("Draft", "draft", "C", "A", published=False)
        self.db.create_post("Published", "pub", "C", "A", published=True)
        published = self.db.list_posts(published_only=True)
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0].title, "Published")

    def test_list_posts_by_author(self):
        self.db.create_post("P1", "p1", "C", "Alice")
        self.db.create_post("P2", "p2", "C", "Bob")
        alice_posts = self.db.list_posts(author="Alice")
        self.assertEqual(len(alice_posts), 1)

    def test_update_post(self):
        post = self.db.create_post("Old", "old", "C", "A")
        updated = self.db.update_post(post.id, title="New")
        self.assertEqual(updated.title, "New")

    def test_delete_post_cascades_comments(self):
        post = self.db.create_post("P", "p", "C", "A")
        self.db.create_comment(post.id, "User", "e@e.com", "Nice")
        self.db.delete_post(post.id)
        self.assertEqual(len(self.db.list_comments(post_id=post.id)), 0)

    def test_create_comment(self):
        post = self.db.create_post("P", "p", "C", "A")
        comment = self.db.create_comment(post.id, "User", "e@e.com", "Great!")
        self.assertIsNotNone(comment)
        self.assertFalse(comment.approved)

    def test_create_comment_nonexistent_post(self):
        comment = self.db.create_comment("fake", "User", "e@e.com", "Text")
        self.assertIsNone(comment)

    def test_approve_comment(self):
        post = self.db.create_post("P", "p", "C", "A")
        comment = self.db.create_comment(post.id, "User", "e@e.com", "Text")
        approved = self.db.approve_comment(comment.id)
        self.assertTrue(approved.approved)

    def test_list_comments_approved_only(self):
        post = self.db.create_post("P", "p", "C", "A")
        c1 = self.db.create_comment(post.id, "U1", "e@e.com", "T1")
        self.db.create_comment(post.id, "U2", "e@e.com", "T2")
        self.db.approve_comment(c1.id)
        approved = self.db.list_comments(post_id=post.id, approved_only=True)
        self.assertEqual(len(approved), 1)

    def test_get_stats(self):
        stats = self.db.get_stats()
        self.assertIn("total_posts", stats)
        self.assertIn("total_comments", stats)


class TestPostRouter(unittest.TestCase):
    """Test post API endpoint handlers."""

    def setUp(self):
        self.db = Database()
        self.router = PostRouter(self.db)

    def test_create_post_returns_201(self):
        response = self.router.create_post("Title", "Content", "Author")
        self.assertEqual(response["status"], 201)

    def test_get_post_returns_200(self):
        create = self.router.create_post("T", "C", "A")
        response = self.router.get_post(create["data"]["id"])
        self.assertEqual(response["status"], 200)

    def test_get_nonexistent_post(self):
        response = self.router.get_post("fake-id")
        self.assertEqual(response["status"], 404)

    def test_list_posts(self):
        self.router.create_post("T1", "C1", "A")
        self.router.create_post("T2", "C2", "A")
        response = self.router.list_posts()
        self.assertEqual(response["count"], 2)

    def test_update_post_content(self):
        create = self.router.create_post("T", "Old Content", "A")
        response = self.router.update_post(create["data"]["id"], content="New Content")
        self.assertEqual(response["status"], 200)
        self.assertIn("New Content", response["data"]["content"])

    def test_publish_post(self):
        create = self.router.create_post("T", "C", "A")
        response = self.router.publish_post(create["data"]["id"])
        self.assertEqual(response["status"], 200)
        self.assertTrue(response["data"]["published"])

    def test_delete_post(self):
        create = self.router.create_post("T", "C", "A")
        response = self.router.delete_post(create["data"]["id"])
        self.assertEqual(response["status"], 200)

    def test_generate_slug(self):
        slug = PostRouter._generate_slug("Hello World! This is a Test")
        self.assertEqual(slug, "hello-world-this-is-a-test")

    def test_generate_slug_special_chars(self):
        slug = PostRouter._generate_slug("Python 3.10: What's New?")
        self.assertNotIn(" ", slug)
        self.assertNotIn(":", slug)


class TestCommentRouter(unittest.TestCase):
    """Test comment API endpoint handlers."""

    def setUp(self):
        self.db = Database()
        self.post_router = PostRouter(self.db)
        self.comment_router = CommentRouter(self.db)
        create = self.post_router.create_post("Test Post", "Content", "Author")
        self.post_id = create["data"]["id"]

    def test_create_comment(self):
        response = self.comment_router.create_comment(
            self.post_id, "User", "u@test.com", "Nice!"
        )
        self.assertEqual(response["status"], 201)

    def test_create_comment_nonexistent_post(self):
        response = self.comment_router.create_comment(
            "fake", "User", "u@test.com", "Text"
        )
        self.assertEqual(response["status"], 404)

    def test_approve_comment(self):
        create = self.comment_router.create_comment(
            self.post_id, "User", "u@test.com", "Text"
        )
        response = self.comment_router.approve_comment(create["data"]["id"])
        self.assertEqual(response["status"], 200)


class TestMarkdownRenderer(unittest.TestCase):
    """Test markdown to HTML conversion."""

    def setUp(self):
        self.renderer = MarkdownRenderer()

    def test_empty_input(self):
        self.assertEqual(self.renderer.render(""), "")

    def test_heading_h1(self):
        result = self.renderer.render("# Title")
        self.assertIn("<h1>Title</h1>", result)

    def test_heading_h2(self):
        result = self.renderer.render("## Subtitle")
        self.assertIn("<h2>Subtitle</h2>", result)

    def test_bold(self):
        result = self.renderer.render("This is **bold** text")
        self.assertIn("<strong>bold</strong>", result)

    def test_italic(self):
        result = self.renderer.render("This is *italic* text")
        self.assertIn("<em>italic</em>", result)

    def test_inline_code(self):
        result = self.renderer.render("Use `print()` function")
        self.assertIn("<code>print()</code>", result)

    def test_code_block(self):
        md = "```python\nprint('hello')\n```"
        result = self.renderer.render(md)
        self.assertIn('<pre><code class="language-python">', result)

    def test_link(self):
        result = self.renderer.render("[Click here](https://example.com)")
        self.assertIn('<a href="https://example.com">Click here</a>', result)

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2"
        result = self.renderer.render(md)
        self.assertIn("<ul>", result)
        self.assertIn("<li>Item 1</li>", result)

    def test_ordered_list(self):
        md = "1. First\n2. Second"
        result = self.renderer.render(md)
        self.assertIn("<ol>", result)
        self.assertIn("<li>First</li>", result)

    def test_blockquote(self):
        result = self.renderer.render("> Important note")
        self.assertIn("<blockquote>Important note</blockquote>", result)

    def test_paragraph(self):
        result = self.renderer.render("Just a paragraph")
        self.assertIn("<p>Just a paragraph</p>", result)

    def test_horizontal_rule(self):
        result = self.renderer.render("---")
        self.assertIn("<hr>", result)


if __name__ == "__main__":
    unittest.main()
