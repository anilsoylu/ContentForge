"""Core module - constants, errors, data models and config."""
from core.config import load_api_key, load_config, save_default_config, validate_config
from core.constants import (
    API_TIMEOUT,
    AVAILABLE_MODELS,
    DEFAULT_CONFIG_PATH,
    DEFAULT_MODEL,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SYSTEM_PROMPT,
    MARKDOWN_FENCE_PATTERN,
    MAX_RETRIES,
    OPENROUTER_API_URL,
    REQUIRED_CONFIG_FIELDS,
    RETRY_DELAY,
    UPPERCASE_WORD_PATTERN,
)
from core.exceptions import (
    APIConnectionError,
    APIError,
    APIKeyError,
    APIResponseError,
    ConfigError,
    ConfigNotFoundError,
    ConfigValidationError,
    ContentGenerationError,
    SEOGeneratorError,
)
from core.models import (
    ContentConfig,
    GeneratedContent,
    PlaceholderConfig,
    Section,
    SEOConfig,
    SiteConfig,
    TableColumn,
    TableConfig,
    TableRow,
)

__all__ = [
    # Config
    "load_api_key",
    "load_config",
    "save_default_config",
    "validate_config",
    # Constants
    "API_TIMEOUT",
    "AVAILABLE_MODELS",
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_MODEL",
    "DEFAULT_OUTPUT_DIR",
    "DEFAULT_SYSTEM_PROMPT",
    "MARKDOWN_FENCE_PATTERN",
    "MAX_RETRIES",
    "OPENROUTER_API_URL",
    "REQUIRED_CONFIG_FIELDS",
    "RETRY_DELAY",
    "UPPERCASE_WORD_PATTERN",
    # Exceptions
    "APIConnectionError",
    "APIError",
    "APIKeyError",
    "APIResponseError",
    "ConfigError",
    "ConfigNotFoundError",
    "ConfigValidationError",
    "ContentGenerationError",
    "SEOGeneratorError",
    # Models
    "ContentConfig",
    "GeneratedContent",
    "PlaceholderConfig",
    "Section",
    "SEOConfig",
    "SiteConfig",
    "TableColumn",
    "TableConfig",
    "TableRow",
]
