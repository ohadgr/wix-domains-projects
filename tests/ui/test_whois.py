from playwright.sync_api import Page, expect


WHOIS_URL = "https://www.wix.com/domains/whois"
DOMAIN = "lotus-music.com"


def test_whois_registered_domain(page: Page):
    # Arrange: Open WHOIS lookup page
    page.goto(
        WHOIS_URL,
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

    search_input.fill(DOMAIN)
    expect(search_input).to_have_value(DOMAIN)

    expect(search_button).to_be_visible()
    expect(search_button).to_be_enabled()

    search_button.click()

    # Assert: Verify actual WHOIS registrar information
    registrar = page.get_by_text(
        "REG.RU",
        exact=False,
    ).first

    expect(registrar).to_be_visible(timeout=15000)