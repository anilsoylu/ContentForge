"""Config loading and validation."""
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from core.constants import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_MODEL,
    REQUIRED_CONFIG_FIELDS,
)
from core.exceptions import (
    APIKeyError,
    ConfigNotFoundError,
    ConfigValidationError,
)
from core.models import (
    ContentConfig,
    PlaceholderConfig,
    Section,
    SEOConfig,
    SiteConfig,
    TableColumn,
    TableConfig,
)


def load_api_key() -> str:
    """Load API key from .env file."""
    load_dotenv()
    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    if not api_key:
        raise APIKeyError("OPEN_ROUTER_API_KEY not found! Check your .env file.")
    return api_key


def validate_config(data: dict) -> None:
    """Validate config data."""
    if "sections" not in data:
        raise ConfigValidationError(
            "Old config format not supported! "
            "New format requires 'sections' field. "
            "Example: python main.py --init"
        )

    for field in REQUIRED_CONFIG_FIELDS:
        if field not in data:
            raise ConfigValidationError(f"Missing '{field}' field in config!")

    # Validate output format
    output = data.get("output", "html")
    if output not in ("html", "md"):
        raise ConfigValidationError(
            f"Invalid output format: '{output}'. Must be 'html' or 'md'"
        )

    # Validate language
    language = data.get("language", "English")
    if not isinstance(language, str) or not language.strip():
        raise ConfigValidationError("Language must be a non-empty string")


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> ContentConfig:
    """Load YAML config file and return ContentConfig."""
    path = Path(config_path)
    if not path.exists():
        raise ConfigNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    validate_config(data)

    sections = [
        Section(
            heading=s["heading"],
            words=s.get("words", 100)
        )
        for s in data["sections"]
    ]

    # Table config
    table_data = data.get("table", {})
    if isinstance(table_data, dict):
        columns = []
        for col in table_data.get("columns", []):
            columns.append(TableColumn(
                name=col.get("name", ""),
                header=col.get("header", ""),
                placeholder=col.get("placeholder", ""),
                type=col.get("type", "text")
            ))
        table = TableConfig(
            enabled=table_data.get("enabled", False),
            rows=table_data.get("rows", 0),
            columns=columns if columns else TableConfig().get_default_columns()
        )
    else:
        table = TableConfig()

    # Placeholder config
    placeholder_data = data.get("placeholders", {})
    placeholders = PlaceholderConfig(
        item_prefix=placeholder_data.get("item_prefix", "ITEM"),
        value_prefix=placeholder_data.get("value_prefix", "VALUE")
    )

    # SEO config
    seo_data = data.get("seo", {})
    seo = SEOConfig(
        primary_keyword=seo_data.get("primary_keyword", ""),
        secondary_keywords=seo_data.get("secondary_keywords", []),
        keyword_density=seo_data.get("keyword_density", 2.0),
        tone=seo_data.get("tone", "informative"),
        target_audience=seo_data.get("target_audience", "")
    )

    # Site config
    site_data = data.get("site", {})
    site = SiteConfig(
        name=site_data.get("name", ""),
        url=site_data.get("url", ""),
        author=site_data.get("author", "")
    )

    return ContentConfig(
        title=data.get("title", ""),
        intro_words=data.get("intro_words", 60),
        conclusion_words=data.get("conclusion_words", 50),
        sections=sections,
        table=table,
        model=data.get("model", DEFAULT_MODEL),
        placeholders=placeholders,
        seo=seo,
        site=site,
        system_prompt=data.get("system_prompt", ""),
        output=data.get("output", "html"),
        language=data.get("language", "English")
    )


def save_default_config(config_path: str = DEFAULT_CONFIG_PATH) -> None:
    """Create example config file."""
    default_config = {
        "site": {
            "name": "MySite",
            "url": "https://example.com",
            "author": "Content Team"
        },
        "title": "Example Title - Write Your Own Topic",
        "intro_words": 60,
        "conclusion_words": 50,
        "seo": {
            "primary_keyword": "main keyword",
            "secondary_keywords": [
                "secondary keyword 1",
                "secondary keyword 2"
            ],
            "keyword_density": 2.0,
            "tone": "informative",
            "target_audience": "Define your target audience"
        },
        "sections": [
            {"heading": "First Section Heading", "words": 120},
            {"heading": "Second Section Heading", "words": 120},
            {"heading": "Third Section Heading", "words": 100}
        ],
        "table": {
            "enabled": True,
            "rows": 5,
            "columns": [
                {"name": "item", "header": "Item", "placeholder": "ITEM"},
                {"name": "value", "header": "Value", "placeholder": "VALUE"},
                {"name": "feature", "header": "Feature", "placeholder": "FEATURE"},
                {"name": "rating", "header": "Rating", "placeholder": "RATING", "type": "stars"}
            ]
        },
        "model": "openai/gpt-4o-mini",
        "output": "html",
        "language": "English",
        "placeholders": {
            "item_prefix": "ITEM",
            "value_prefix": "VALUE"
        }
    }
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(default_config, f, allow_unicode=True, default_flow_style=False)
    print(f"   ✓ Example config created: {config_path}")
