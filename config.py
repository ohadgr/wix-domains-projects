"""Centralized API configuration. Values can be overridden via environment variables."""
import os

API_BASE_URL = os.getenv("WIX_API_BASE_URL", "https://www.wixapis.com")
AVAILABILITY_PATH = "/domain-search/v2/check-domain-availability"
AVAILABILITY_URL = f"{API_BASE_URL}{AVAILABILITY_PATH}"

REQUEST_TIMEOUT_SECONDS = 15

# Observed registered during exploration; availability is re-checked by the test itself.
REGISTERED_DOMAIN = "lotus-music.com"

API_KEY_ENV_VAR = "WIX_API_KEY"
