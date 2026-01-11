"""Custom exception classes."""


class SEOGeneratorError(Exception):
    """Base exception class."""
    pass


class ConfigError(SEOGeneratorError):
    """Config loading or validation error."""
    pass


class ConfigNotFoundError(ConfigError):
    """Config file not found."""
    pass


class ConfigValidationError(ConfigError):
    """Config validation error."""
    pass


class APIError(SEOGeneratorError):
    """API call error."""
    pass


class APIKeyError(APIError):
    """API key not found or invalid."""
    pass


class APIConnectionError(APIError):
    """API connection error."""
    pass


class APIResponseError(APIError):
    """API response error."""
    pass


class ContentGenerationError(SEOGeneratorError):
    """Content generation error."""
    pass
