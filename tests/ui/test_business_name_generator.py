
import re

from playwright.sync_api import Page, expect

from config import PagePath, page_url


BUSINESS_DESCRIPTION = (
    "An online music store selling guitars, "
    "musical instruments, and accessories."
)


def test_business_name_generator_shows_names_and_domains(page: Page):
    # Arrange: Open Business Name Generator
    page.goto(
        page_url(PagePath.BUSINESS_NAME_GENERATOR),
        wait_until="domcontentloaded",
        timeout=30000,
    )

    description_input = page.locator(
        "textarea[placeholder^='e.g. I own']"
    )

    generate_button = page.get_by_role(
        "button",
        name="Generate Names",
    )

    # Assert: Generator is ready
    expect(description_input).to_be_visible(timeout=15000)
    expect(generate_button).to_be_enabled()

    # Wait for client-side hydration. The textarea is server-rendered and React
    # attaches ~1s later, resetting any value filled before that (verified by
    # polling input_value() and the element's __react* properties).
    description_input.evaluate_handle(
        "el => new Promise(resolve => {"
        "  const hydrated = () => Object.keys(el).some(k => k.startsWith('__react'));"
        "  const check = () => hydrated() ? resolve(true) : requestAnimationFrame(check);"
        "  check();"
        "})"
    )

    # Act: Enter business description
    description_input.fill(BUSINESS_DESCRIPTION)
    expect(description_input).to_have_value(BUSINESS_DESCRIPTION)

    # Act: Generate names
    generate_button.click()

    # Assert: Results page is opened
    expect(page).to_have_url(
        re.compile(r"/domain/result/bng"),
        timeout=30000,
    )

    # Assert: Business names section is displayed
    expect(
        page.get_by_text("Choose a business name", exact=False)
    ).to_be_visible(timeout=30000)

    # Assert: Domain suggestions section is displayed
    expect(
        page.get_by_text(
            "Claim the perfect domain for",
            exact=False,
        )
    ).to_be_visible(timeout=30000)

    # Assert: At least one domain purchase action exists
    expect(
        page.get_by_role(
            "button",
            name="Get It",
            exact=True,
        ).first
    ).to_be_visible(timeout=30000)
