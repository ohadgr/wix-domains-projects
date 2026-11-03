import re

from playwright.sync_api import Page, expect

from config import PagePath, page_url
from testdata import REGISTERED_DOMAIN as DOMAIN



def test_whois_registered_domain(page: Page):
    # Arrange: Open WHOIS lookup page
    page.goto(
        page_url(PagePath.WHOIS),
        wait_until="domcontentloaded",
        timeout=30000,
    )

    search_input = page.get_by_role(
        "textbox",
        name="Enter a domain name or URL",
    ).first

    search_button = page.get_by_role(
        "button",
        name="Search Domains",
        exact=True,
    ).first

    # Act: Search for a registered domain
    expect(search_input).to_be_visible(timeout=15000)
    expect(search_input).to_be_enabled()

    # Wait for client-side hydration; a value filled before React attaches is reset
    # (same behavior verified on the Business Name Generator page).
    search_input.evaluate_handle(
        "el => new Promise(resolve => {"
        "  const hydrated = () => Object.keys(el).some(k => k.startsWith('__react'));"
        "  const check = () => hydrated() ? resolve(true) : requestAnimationFrame(check);"
        "  check();"
        "})"
    )

    search_input.fill(DOMAIN)
    expect(search_input).to_have_value(DOMAIN)

    expect(search_button).to_be_visible()
    expect(search_button).to_be_enabled()

    search_button.click()
    expect(page).to_have_url(
        re.compile(r"/domain/result/whois\?query=" + re.escape(DOMAIN)),
        timeout=30000,
    )

    # Assert: Verify actual WHOIS registrar information
    registrar = page.get_by_text(
        "REG.RU",
        exact=False,
    ).first

    expect(registrar).to_be_visible(timeout=45000)
