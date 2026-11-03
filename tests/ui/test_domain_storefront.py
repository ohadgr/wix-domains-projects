import re

from playwright.sync_api import Page, expect

from config import PagePath, page_url
from testdata import REGISTERED_DOMAIN as DOMAIN



def test_storefront_search_shows_registered_domain(page: Page):
    page.goto(page_url(PagePath.STOREFRONT), wait_until="domcontentloaded", timeout=30000)

    # The page renders two visible search boxes; after client-side load their role
    # becomes "searchbox". Use the first visible one.
    search_input = (
        page.get_by_role("searchbox", name="Type the domain you want")
        .locator("visible=true")
        .first
    )
    search_button = (
        page.get_by_role("button", name="Search Domains", exact=True)
        .locator("visible=true")
        .first
    )
    expect(search_input).to_be_visible(timeout=15000)

    # Documented workaround: the input is server-rendered and a value filled before
    # React attaches is discarded (the click then does nothing). Wait for hydration
    # via __react* element properties; no public "ready" signal was found.
    search_input.evaluate_handle(
        "el => new Promise(resolve => {"
        "  const hydrated = () => Object.keys(el).some(k => k.startsWith('__react'));"
        "  const check = () => hydrated() ? resolve(true) : requestAnimationFrame(check);"
        "  check();"
        "})"
    )
    search_input.fill(DOMAIN)
    expect(search_input).to_have_value(DOMAIN)

    # Act: search, capturing the availability call the UI makes
    with page.expect_response(
        lambda r: "check-domain-availability" in r.url
        and f"domain={DOMAIN}" in r.url,
        timeout=30000,
    ) as response_info:
        search_button.click()
    api_response = response_info.value

    # Assert: results page and user-visible status
    expect(page).to_have_url(re.compile(r"/domain/result/"), timeout=30000)
    expect(
        page.get_by_text(f"{DOMAIN} is already registered", exact=False)
    ).to_be_visible(timeout=30000)

    # Assert: the UI status is consistent with the availability response
    assert api_response.status == 200, f"Unexpected status {api_response.status}"
    availability = api_response.json()["availability"]
    assert availability["domain"] == DOMAIN
    assert availability["available"] is False, (
        "UI says registered but the availability response says available"
    )
