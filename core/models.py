"""Data models - Dataclass definitions."""
from dataclasses import dataclass, field


@dataclass
class Section:
    """Section configuration."""
    heading: str
    words: int = 100


@dataclass
class TableColumn:
    """Dynamic table column."""
    name: str
    header: str
    placeholder: str = ""
    type: str = "text"  # text, stars


@dataclass
class TableConfig:
    """Table configuration."""
    enabled: bool = False
    rows: int = 0
    columns: list[TableColumn] = field(default_factory=list)

    def get_default_columns(self) -> list[TableColumn]:
        """Return default columns."""
        return [
            TableColumn("item", "Item", "ITEM"),
            TableColumn("value", "Value", "VALUE"),
            TableColumn("feature", "Feature", "FEATURE"),
            TableColumn("rating", "Rating", "RATING", "stars"),
        ]


@dataclass
class PlaceholderConfig:
    """Placeholder settings."""
    item_prefix: str = "ITEM"
    value_prefix: str = "VALUE"


@dataclass
class SiteConfig:
    """Site information."""
    name: str = ""
    url: str = ""
    author: str = ""


@dataclass
class SEOConfig:
    """SEO configuration."""
    primary_keyword: str = ""
    secondary_keywords: list[str] = field(default_factory=list)
    keyword_density: float = 2.0
    tone: str = "informative"  # informative, conversational, professional
    target_audience: str = ""

    @property
    def all_keywords(self) -> list[str]:
        """Return all keywords (for highlighting)."""
        keywords = []
        if self.primary_keyword:
            keywords.append(self.primary_keyword)
        keywords.extend(self.secondary_keywords)
        return keywords


@dataclass
class ContentConfig:
    """Main content configuration."""
    title: str
    intro_words: int
    conclusion_words: int
    sections: list[Section]
    table: TableConfig
    model: str
    placeholders: PlaceholderConfig
    seo: SEOConfig = field(default_factory=SEOConfig)
    site: SiteConfig = field(default_factory=SiteConfig)
    system_prompt: str = ""  # Optional custom system prompt
    output: str = "html"  # Output format: "html" or "md"
    language: str = "English"  # Content language

    @property
    def headings(self) -> list[str]:
        """Return section headings."""
        return [s.heading for s in self.sections]

    @property
    def total_words(self) -> int:
        """Total target word count."""
        return (
            self.intro_words
            + self.conclusion_words
            + sum(s.words for s in self.sections)
        )

    @property
    def api_call_count(self) -> int:
        """Total API call count."""
        base = 2 + len(self.sections)
        if self.table.enabled and self.table.rows > 0:
            base += 1
        return base


@dataclass
class TableRow:
    """Dynamic table row data."""
    values: dict[str, str] = field(default_factory=dict)

    def get(self, column_name: str, default: str = "") -> str:
        """Get column value."""
        return self.values.get(column_name, default)


@dataclass
class GeneratedContent:
    """Generated content."""
    intro: str = ""
    table_html: str = ""
    table_md: str = ""  # Markdown table
    sections: list[str] = field(default_factory=list)
    conclusion: str = ""
