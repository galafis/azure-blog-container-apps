"""Simple markdown to HTML converter.

Provides basic markdown rendering without external dependencies.
Supports headers, bold, italic, code blocks, inline code, links,
images, unordered lists, ordered lists, blockquotes, and paragraphs.
"""

import re


class MarkdownRenderer:
    """Converts markdown text to HTML.

    Supports a subset of common markdown syntax elements
    suitable for rendering blog post content.
    """

    def render(self, markdown_text: str) -> str:
        """Convert markdown text to HTML.

        Args:
            markdown_text: The markdown-formatted text to convert.

        Returns:
            The rendered HTML string.
        """
        if not markdown_text:
            return ""

        lines = markdown_text.split("\n")
        html_lines = []
        in_code_block = False
        in_list = False
        list_type = None

        for line in lines:
            # Fenced code blocks
            if line.strip().startswith("```"):
                if in_code_block:
                    html_lines.append("</code></pre>")
                    in_code_block = False
                else:
                    lang = line.strip()[3:].strip()
                    if lang:
                        html_lines.append(f'<pre><code class="language-{lang}">')
                    else:
                        html_lines.append("<pre><code>")
                    in_code_block = True
                continue

            if in_code_block:
                html_lines.append(self._escape_html(line))
                continue

            # Close list if line is not a list item
            if in_list and not self._is_list_item(line):
                tag = "ol" if list_type == "ordered" else "ul"
                html_lines.append(f"</{tag}>")
                in_list = False
                list_type = None

            # Headers
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                text = self._process_inline(header_match.group(2))
                html_lines.append(f"<h{level}>{text}</h{level}>")
                continue

            # Horizontal rule
            if re.match(r"^(-{3,}|_{3,}|\*{3,})$", line.strip()):
                html_lines.append("<hr>")
                continue

            # Blockquote
            if line.startswith(">"):
                text = self._process_inline(line[1:].strip())
                html_lines.append(f"<blockquote>{text}</blockquote>")
                continue

            # Unordered list
            ul_match = re.match(r"^[\s]*[-*+]\s+(.+)$", line)
            if ul_match:
                if not in_list or list_type != "unordered":
                    if in_list:
                        tag = "ol" if list_type == "ordered" else "ul"
                        html_lines.append(f"</{tag}>")
                    html_lines.append("<ul>")
                    in_list = True
                    list_type = "unordered"
                text = self._process_inline(ul_match.group(1))
                html_lines.append(f"<li>{text}</li>")
                continue

            # Ordered list
            ol_match = re.match(r"^[\s]*\d+\.\s+(.+)$", line)
            if ol_match:
                if not in_list or list_type != "ordered":
                    if in_list:
                        tag = "ol" if list_type == "ordered" else "ul"
                        html_lines.append(f"</{tag}>")
                    html_lines.append("<ol>")
                    in_list = True
                    list_type = "ordered"
                text = self._process_inline(ol_match.group(1))
                html_lines.append(f"<li>{text}</li>")
                continue

            # Empty line
            if not line.strip():
                html_lines.append("")
                continue

            # Paragraph
            text = self._process_inline(line)
            html_lines.append(f"<p>{text}</p>")

        # Close any open list
        if in_list:
            tag = "ol" if list_type == "ordered" else "ul"
            html_lines.append(f"</{tag}>")

        if in_code_block:
            html_lines.append("</code></pre>")

        return "\n".join(html_lines)

    def _process_inline(self, text: str) -> str:
        """Process inline markdown elements.

        Handles bold, italic, inline code, links, and images.

        Args:
            text: The text line to process.

        Returns:
            The text with inline elements converted to HTML.
        """
        # Images: ![alt](url)
        text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)

        # Links: [text](url)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

        # Bold: **text** or __text__
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)

        # Italic: *text* or _text_
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", text)

        # Inline code: `code`
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

        return text

    @staticmethod
    def _is_list_item(line: str) -> bool:
        """Check if a line is a list item."""
        return bool(
            re.match(r"^[\s]*[-*+]\s+", line)
            or re.match(r"^[\s]*\d+\.\s+", line)
        )

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters in text."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
