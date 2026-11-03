import os

import pytest
import requests

import config


@pytest.fixture(scope="session")
def api_key():
    key = os.getenv(config.API_KEY_ENV_VAR)
    if not key:
        pytest.skip(f"{config.API_KEY_ENV_VAR} is not set; skipping authenticated API tests")
    return key


@pytest.fixture
def check_availability(api_key):
    """Authenticated GET to check-domain-availability. Returns requests.Response."""

    def _call(domain):
        return requests.get(
            config.AVAILABILITY_URL,
            params={"domain": domain},
            headers={"Authorization": api_key},
            timeout=config.REQUEST_TIMEOUT_SECONDS,
        )

    return _call


@pytest.fixture
def check_availability_unauthenticated():
    """Same GET without any Authorization header."""

    def _call(domain):
        return requests.get(
            config.AVAILABILITY_URL,
            params={"domain": domain},
            timeout=config.REQUEST_TIMEOUT_SECONDS,
        )

    return _call
