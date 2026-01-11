"""HTML generation functions."""
import re
from core.models import GeneratedContent, TableColumn, TableRow


def value_to_stars(value: str) -> str:
    """Convert rating value to stars."""
    try:
        num = int(value.strip())
        return "⭐" * min(max(num, 1), 5)
    except ValueError:
        return value


def build_table_html(rows: list[TableRow], columns: list[TableColumn]) -> str:
    """Build HTML from dynamic table data."""
    if not rows or not columns:
        return ""

    lines = [
        '<table class="table table-striped">',
        '  <thead>',
        '    <tr>',
    ]

    # Dynamic headers
    for col in columns:
        lines.append(f'      <th>{col.header}</th>')

    lines.extend([
        '    </tr>',
        '  </thead>',
        '  <tbody>'
    ])

    # Rows
    for row in rows:
        lines.append('    <tr>')
        for col in columns:
            value = row.get(col.name, "")
            # Convert to stars if column type is stars
            if col.type == "stars":
                value = value_to_stars(value)
            lines.append(f'      <td>{value}</td>')
        lines.append('    </tr>')

    lines.extend([
        '  </tbody>',
        '</table>'
    ])

    return '\n'.join(lines)


def highlight_keywords(text: str, keywords: list[str]) -> str:
    """Highlight only specified keywords."""
    if not keywords:
        return text

    for keyword in keywords:
        # Case-insensitive search, preserve original case
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(lambda m: f'<b>{m.group()}</b>', text)

    return text


def text_to_html(text: str, keywords: list[str] | None = None) -> str:
    """Convert plain text to HTML paragraphs."""
    text = text.strip()
    if not text:
        return ""

    paragraphs = []
    current_list: list[str] = []
    current_para: list[str] = []

    def flush_para():
        if current_para:
            paragraphs.append(f"<p>{' '.join(current_para)}</p>")
            current_para.clear()

    def flush_list():
        if current_list:
            items = "\n".join(f"  <li>{item}</li>" for item in current_list)
            paragraphs.append(f"<ul>\n{items}\n</ul>")
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

    html = "\n".join(paragraphs)

    # Highlight only specified keywords
    if keywords:
        html = highlight_keywords(html, keywords)

    return html


def build_full_html(
    title: str,
    content: GeneratedContent,
    headings: list[str],
    keywords: list[str] | None = None,
    table_header: str = "Comparison",
    conclusion_header: str = "Conclusion"
) -> str:
    """Combine all content into HTML format."""
    lines = [
        f"<h1>{title}</h1>",
        "",
        '<div class="intro">',
        text_to_html(content.intro, keywords),
        '</div>',
        ""
    ]

    if content.table_html and content.table_html.strip():
        lines.extend([
            '<div class="comparison-table">',
            f'<h2>{table_header}</h2>',
            content.table_html.strip(),
            '</div>',
            ""
        ])

    for heading, section_content in zip(headings, content.sections):
        lines.extend([
            '<section>',
            f'<h2>{heading}</h2>',
            text_to_html(section_content, keywords),
            '</section>',
            ""
        ])

    lines.extend([
        '<div class="conclusion">',
        f'<h2>{conclusion_header}</h2>',
        text_to_html(content.conclusion, keywords),
        '</div>'
    ])

    return '\n'.join(lines)
