
import config


def _availability(response):
    """Extract and validate the availability object."""
    body = response.json()

    assert isinstance(body, dict), (
        f"Expected JSON object, got {type(body).__name__}"
    )

    availability = body.get("availability")

    assert isinstance(availability, dict), (
        "Response must contain an 'availability' JSON object"
    )

    return availability


def test_registered_domain_is_unavailable(check_availability):
    """A known registered domain must not be available."""
    response = check_availability(config.REGISTERED_DOMAIN)

    assert response.status_code == 200, (
        f"Expected HTTP 200, got {response.status_code}"
    )

    availability = _availability(response)

    assert availability.get("domain") == config.REGISTERED_DOMAIN, (
        f"Expected domain {config.REGISTERED_DOMAIN}, "
        f"got {availability.get('domain')!r}"
    )

    assert availability.get("available") is False, (
        f"Expected registered domain {config.REGISTERED_DOMAIN} "
        f"to be unavailable, "
        f"got {availability.get('available')!r}"
    )


def test_observed_availability_response_contract(check_availability):
    """
    Validate the observed API response structure.

    This is not a complete official schema validation.
    """
    response = check_availability(config.REGISTERED_DOMAIN)

    assert response.status_code == 200, (
        f"Expected HTTP 200, got {response.status_code}"
    )

    availability = _availability(response)

    assert isinstance(availability.get("domain"), str), (
        "'domain' must be a string"
    )

    assert isinstance(availability.get("available"), bool), (
        "'available' must be a boolean"
    )

    assert isinstance(availability.get("premium"), bool), (
        "'premium' must be a boolean"
    )

    if "premiumType" in availability:
        assert isinstance(availability["premiumType"], str), (
            "'premiumType' must be a string"
        )


def test_unauthenticated_availability_response(
    check_availability_unauthenticated,
):
    """
    Verify observed behavior without an Authorization header.

    Independent curl and requests calls returned HTTP 200.
    Whether authentication is required remains to be clarified
    against the official API documentation.
    """
    response = check_availability_unauthenticated(
        config.REGISTERED_DOMAIN
    )

    assert response.status_code == 200, (
        f"Expected observed HTTP 200 without Authorization, "
        f"got {response.status_code}"
    )

    availability = _availability(response)

    assert availability.get("domain") == config.REGISTERED_DOMAIN, (
        f"Expected domain {config.REGISTERED_DOMAIN}, "
        f"got {availability.get('domain')!r}"
    )

    assert availability.get("available") is False, (
        "Known registered domain should be unavailable"
    )
