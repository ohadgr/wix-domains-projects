"""Centralized API configuration. Values can be overridden via environment variables."""
import os
from enum import Enum

API_BASE_URL = os.getenv("WIX_API_BASE_URL", "https://www.wixapis.com")
AVAILABILITY_PATH = "/domain-search/v2/check-domain-availability"
AVAILABILITY_URL = f"{API_BASE_URL}{AVAILABILITY_PATH}"

# Web UI base URL (Production by default; override for other environments).
WEB_BASE_URL = os.getenv("WIX_WEB_BASE_URL", "https://www.wix.com")


class PagePath(str, Enum):
    """Paths of the three web UI entry points."""

    STOREFRONT = "/domains"
    BUSINESS_NAME_GENERATOR = "/tools/business-name-generator"
    WHOIS = "/domains/whois"


def page_url(path: PagePath) -> str:
    return f"{WEB_BASE_URL}{path.value}"


REQUEST_TIMEOUT_SECONDS = 15

API_KEY_ENV_VAR = "WIX_API_KEY"
