"""Markdown generation functions."""
import re
from core.models import GeneratedContent, TableColumn, TableRow


def value_to_stars(value: str) -> str:
    """Convert rating value to stars."""
    try:
        num = int(value.strip())
        return "⭐" * min(max(num, 1), 5)
    except ValueError:
        return value


def build_table_md(rows: list[TableRow], columns: list[TableColumn]) -> str:
    """Build Markdown table from dynamic table data."""
    if not rows or not columns:
        return ""

    lines = []

    # Header row
    headers = [col.header for col in columns]
    lines.append("| " + " | ".join(headers) + " |")

    # Separator row
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

    # Data rows
    for row in rows:
        values = []
        for col in columns:
            value = row.get(col.name, "")
            if col.type == "stars":
                value = value_to_stars(value)
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def highlight_keywords_md(text: str, keywords: list[str]) -> str:
    """Highlight keywords with bold markdown (**keyword**)."""
    if not keywords:
        return text

    for keyword in keywords:
        # Case-insensitive search, preserve original case
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(lambda m: f'**{m.group()}**', text)

    return text


def text_to_md(text: str, keywords: list[str] | None = None) -> str:
    """Convert plain text to Markdown paragraphs."""
    text = text.strip()
    if not text:
        return ""

    paragraphs = []
    current_list: list[str] = []
    current_para: list[str] = []

    def flush_para():
        if current_para:
            paragraphs.append(" ".join(current_para))
            current_para.clear()

    def flush_list():
        if current_list:
            items = "\n".join(f"- {item}" for item in current_list)
            paragraphs.append(items)
            current_list.clear()

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            flush_para()
            flush_list()
            continue

        if line.startswith(('• ', '- ', '* ')):
            flush_para()
            current_list.append(line[2:])
        else:
            flush_list()
            current_para.append(line)

    flush_para()
    flush_list()

    md = "\n\n".join(paragraphs)

    # Highlight only specified keywords
    if keywords:
        md = highlight_keywords_md(md, keywords)

    return md


def build_full_md(
    title: str,
    content: GeneratedContent,
    headings: list[str],
    keywords: list[str] | None = None,
    table_header: str = "Comparison"
) -> str:
    """Combine all content into Markdown format."""
    lines = [
        f"# {title}",
        "",
        text_to_md(content.intro, keywords),
        ""
    ]

    if content.table_md and content.table_md.strip():
        lines.extend([
            f"## {table_header}",
            "",
            content.table_md.strip(),
            ""
        ])

    for heading, section_content in zip(headings, content.sections):
        lines.extend([
            f"## {heading}",
            "",
            text_to_md(section_content, keywords),
            ""
        ])

    lines.extend([
        "## Conclusion",
        "",
        text_to_md(content.conclusion, keywords)
    ])

    return "\n".join(lines)
