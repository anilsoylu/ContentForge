"""Constants and compiled regex patterns."""
import re

# API Endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Defaults
DEFAULT_CONFIG_PATH = "config.yaml"
DEFAULT_OUTPUT_DIR = "content"
DEFAULT_MODEL = "openai/gpt-4o-mini"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
API_TIMEOUT = 120  # seconds

# Available models
AVAILABLE_MODELS = {
    "1": ("openai/gpt-4o", "GPT-4o (higher quality, slower)"),
    "2": ("openai/gpt-4o-mini", "GPT-4o-mini (fast, economical)"),
    "3": ("openai/gpt-oss-20b:free", "GPT-OSS-20B (free, 131K context)"),
}

# Compiled regex patterns (for performance)
MARKDOWN_FENCE_PATTERN = re.compile(r'```\w*\s*')
UPPERCASE_WORD_PATTERN = re.compile(r'\b([A-Z]{3,})\b')

# Default system prompt
DEFAULT_SYSTEM_PROMPT = """You are an experienced SEO content writer. You create content that meets Google E-E-A-T standards and provides value to readers.

CORE PRINCIPLES:
- Every sentence should provide concrete value to the reader
- Avoid filler phrases ("as everyone knows", "undoubtedly", "it goes without saying")
- Include concrete examples, numerical data, and practical tips
- Use natural keyword placement, avoid keyword stuffing
- Avoid exaggerated claims ("the best", "absolutely", "must")

FORMAT RULES:
- Only produce content in the requested format
- Do not add explanations, comments, or meta information
- Do not use HTML tags (unless specified otherwise)"""

# Required config fields
REQUIRED_CONFIG_FIELDS = ["title", "intro_words", "conclusion_words", "sections"]
