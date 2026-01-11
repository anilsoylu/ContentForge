"""Text processing helper functions."""
from core.constants import MARKDOWN_FENCE_PATTERN
from core.models import TableColumn, TableRow


def clean_markdown_fences(text: str) -> str:
    """Clean markdown code fences (```html, ``` etc.)."""
    return MARKDOWN_FENCE_PATTERN.sub('', text).strip()


def parse_table_data(raw_data: str, columns: list[TableColumn]) -> list[TableRow]:
    """Parse pipe-separated table data dynamically."""
    rows = []
    for line in raw_data.strip().split('\n'):
        line = line.strip()
        if not line or '|' not in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= len(columns):
            values = {}
            for i, col in enumerate(columns):
                values[col.name] = parts[i] if i < len(parts) else ""
            rows.append(TableRow(values=values))
    return rows


def truncate_to_char_limit(content: str, max_chars: int) -> tuple[str, bool]:
    """
    Truncate content to character limit.
    Returns: (truncated content, was truncated?)
    """
    if len(content) <= max_chars:
        return content, False

    truncated = content[:max_chars]
    last_sentence_end = max(
        truncated.rfind('.'),
        truncated.rfind('!'),
        truncated.rfind('?')
    )

    if last_sentence_end > max_chars * 0.7:
        return truncated[:last_sentence_end + 1], True

    return truncated, True
