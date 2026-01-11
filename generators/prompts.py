"""SEO-focused prompt builder functions."""
from core.models import PlaceholderConfig, SEOConfig, TableConfig


def build_intro_prompt(
    title: str,
    headings: list[str],
    intro_words: int,
    seo: SEOConfig,
    language: str = "English"
) -> str:
    """Build intro paragraph prompt - SEO optimized."""
    topics = ', '.join(headings[:3])

    keyword_instruction = ""
    if seo.primary_keyword:
        keyword_instruction = f"\n- Use the primary keyword ({seo.primary_keyword}) naturally in the first 2 sentences"

    audience_instruction = ""
    if seo.target_audience:
        audience_instruction = f"\n- Target audience: {seo.target_audience}"

    return f'''Write an INTRODUCTION paragraph for a blog post about "{title}".

HOOK STRATEGY (choose one):
- Start with a surprising statistic or fact
- Describe a problem the reader faces
- Ask a curiosity-provoking question

CONTENT REQUIREMENTS:
- Approximately {intro_words} words
- Explain what the article is about and what value it provides to the reader
- Topics to be covered: {topics}{keyword_instruction}{audience_instruction}

AVOID:
- Cliché openings like "In this article"
- Filler phrases like "Nowadays", "In recent years"
- Exaggerated promises

IMPORTANT: Write plain text only. Do not use HTML tags.

LANGUAGE: Write the content in {language}.'''


def build_table_prompt(
    title: str,
    table_config: TableConfig,
    placeholders: PlaceholderConfig,
    language: str = "English"
) -> str:
    """Build comparison table prompt - dynamic columns."""
    row_count = table_config.rows
    columns = table_config.columns

    # Build column info
    column_names = " | ".join(col.name for col in columns)

    # Placeholder rules
    placeholder_rules = []
    for i, col in enumerate(columns):
        if col.placeholder:
            placeholder_rules.append(
                f"- For {col.header} use [{col.placeholder}_1], [{col.placeholder}_2]... placeholders"
            )
    placeholder_text = "\n".join(placeholder_rules) if placeholder_rules else ""

    # Build example row
    example_values = []
    for col in columns:
        if col.placeholder:
            example_values.append(f"[{col.placeholder}_1]")
        elif col.type == "stars":
            example_values.append("4")
        else:
            example_values.append("example")
    example_row = " | ".join(example_values)

    return f'''Provide {row_count} item information for the topic "{title}".

FORMAT: One item per line, separated by pipe (|).
COLUMNS: {column_names}

RULES:
{placeholder_text}
- Use numbers 1-5 for rating column

EXAMPLE OUTPUT:
{example_row}

Write ONLY {row_count} lines of data, nothing else.

LANGUAGE: Write the content in {language}.'''


def _get_section_perspective(heading: str, section_index: int) -> str:
    """Determine unique perspective for each section."""
    perspectives = {
        0: "Basic information and first steps for beginners",
        1: "Practical comparison and evaluation criteria",
        2: "Advanced tips and maximum benefit strategies",
        3: "Common mistakes and how to avoid them",
        4: "Future trends and things to watch out for"
    }
    return perspectives.get(section_index, "In-depth analysis and concrete examples")


def build_section_prompt(
    title: str,
    heading: str,
    section_words: int,
    section_index: int,
    total_sections: int,
    previous_topics: list[str],
    seo: SEOConfig,
    placeholders: PlaceholderConfig,
    language: str = "English"
) -> str:
    """Build section content prompt - SEO optimized."""
    perspective = _get_section_perspective(heading, section_index)

    avoid_topics = ""
    if previous_topics:
        avoid_topics = f"\n- DO NOT REPEAT (already covered): {', '.join(previous_topics)}"

    keyword_instruction = ""
    if seo.primary_keyword:
        keyword_instruction = f"\n- Primary keyword ({seo.primary_keyword}): Use naturally once in this section"

    secondary_instruction = ""
    if seo.secondary_keywords:
        relevant_kw = [kw for kw in seo.secondary_keywords if kw.lower() in heading.lower()]
        if relevant_kw:
            secondary_instruction = f"\n- Related keywords (use naturally): {', '.join(relevant_kw)}"

    tone_map = {
        "informative": "Informative and objective",
        "conversational": "Friendly and conversational",
        "professional": "Professional and formal"
    }
    tone_desc = tone_map.get(seo.tone, "Informative")

    # Placeholder usage
    placeholder_hint = f"[{placeholders.item_prefix}_NAME], [{placeholders.value_prefix}_VALUE]"

    return f'''Write original content about "{heading}".

MAIN TITLE: {title}
SECTION: {section_index + 1}/{total_sections}
PERSPECTIVE: {perspective}
TONE: {tone_desc}

CONTENT REQUIREMENTS:
- Approximately {section_words} words
- At least 1 concrete example or numerical data
- At least 2 practical, actionable tips
- For bullet lists use: "• "{keyword_instruction}{secondary_instruction}
- Use placeholders: {placeholder_hint}

AVOID:{avoid_topics}
- DO NOT REPEAT MAIN TITLE: Don't use "{title}" within the section
- Generic phrases: "quality service", "reliable platform", "professional team"
- Exaggerated claims: "the best", "absolutely", "must", "guaranteed"
- Filler sentences: "as everyone knows", "undoubtedly"

IMPORTANT: Write plain text only. Do not use HTML tags.

LANGUAGE: Write the content in {language}.'''


def build_conclusion_prompt(
    title: str,
    headings: list[str],
    conclusion_words: int,
    seo: SEOConfig,
    language: str = "English"
) -> str:
    """Build conclusion paragraph prompt - SEO optimized."""
    topics = ', '.join(headings)

    keyword_instruction = ""
    if seo.primary_keyword:
        keyword_instruction = f"\n- Use the primary keyword ({seo.primary_keyword}) once more"

    return f'''Write a CONCLUSION paragraph for an article about "{title}".

TOPICS COVERED IN THE ARTICLE: {topics}

CONTENT REQUIREMENTS:
- Approximately {conclusion_words} words
- Summarize main points in 1-2 sentences (synthesis, not repetition)
- Suggest a concrete next step for the reader (CTA)
- End with a positive but realistic tone{keyword_instruction}

AVOID:
- Starting with "In conclusion"
- Repeating exactly what was said in the article
- Exaggerated promises

IMPORTANT: Write plain text only. Do not use HTML tags.

LANGUAGE: Write the content in {language}.'''
