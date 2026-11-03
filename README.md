# Wix Domains — QA Home Assignment

A risk-based quality assessment of Wix Domains: system exploration, test planning, exploratory validation and automated testing with Python, pytest and Playwright.

**Target environment:** Production (public surfaces only; no purchases, payments or registrations)
**Execution date:** November 3, 2026
**Time spent:** started at the first commit, 11:06 (Israel time); final commit time: `[PLACEHOLDER: final commit time]`; total: `[PLACEHOLDER: total hours/minutes]`
**Latest result:** 4 passed, 2 skipped, 0 failed

## 1. Scope and Coverage

| Surface | URL | Coverage |
|---|---|---|
| Domain Storefront | https://www.wix.com/domains | Exploration + network analysis + automated UI test (including UI/availability-response consistency) |
| WHOIS Lookup | https://www.wix.com/domains/whois | Exploration + automated UI test |
| Business Name Generator | https://www.wix.com/tools/business-name-generator | Exploration + automated UI test |
| Public Domain Search API | [Wix Developers](https://dev.wix.com/docs/api-reference/account-level/domains/domain-search/introduction) | 3 API tests: 1 passed, 2 skipped (no `WIX_API_KEY`) |

## 2. Deliverables

| File | Purpose |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Surfaces, observed network calls, inferred flows, unknowns |
| [TEST_PLAN.md](TEST_PLAN.md) | Risk-based strategy, matrix with actual statuses, exclusions |
| [FINDINGS.md](FINDINGS.md) | Five evidence-based findings with severity, priority and classification |
| [AI_LOG.md](AI_LOG.md) | AI usage, corrections and human verification |
| `tests/api/test_domain_availability.py` | Public API tests |
| `tests/ui/test_domain_storefront.py` | Storefront search and UI/API consistency |
| `tests/ui/test_whois.py` | WHOIS lookup |
| `tests/ui/test_business_name_generator.py` | Name generation and domain suggestions |

## 3. Setup

Python 3.9, pytest 8.4.2, Playwright 1.60.0, pytest-playwright 0.7.1, requests (pinned in `requirements.txt`).

```bash
git clone https://github.com/ohadgr/wix-domains-projects.git
cd wix-domains-projects
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### API key

Authenticated API tests read the key from the `WIX_API_KEY` environment variable. **`.env` files are not loaded automatically** (no `python-dotenv`); export the variable in the shell that runs pytest. `.env` is git-ignored. Never commit keys.

```bash
export WIX_API_KEY="your-api-key"
```

Without it, the two authenticated tests are **skipped** (not failed). The missing-authentication test runs without a key. A manual run with the available key reportedly returned `400 INVALID_TARGET_ACCOUNT_ID`, so account permissions remain unverified (see F-02).

## 4. Running Tests

Single command for the whole suite:

```bash
python -m pytest -v
```

Other options: `python -m pytest tests/api -v`, `python -m pytest tests/ui -v --headed`.

Tests use public Production URLs by default. No Dev or Staging environment was available, so non-Production execution was not validated.

### Configuration and Test Data

| Item | Location | Notes |
|---|---|---|
| `WIX_WEB_BASE_URL` | `config.py` | Web UI base URL; defaults to `https://www.wix.com` |
| `WIX_API_BASE_URL` | `config.py` | API base URL; defaults to `https://www.wixapis.com` |
| `PagePath` | `config.py` | Enum of the three UI entry points: `STOREFRONT` (`/domains`), `BUSINESS_NAME_GENERATOR` (`/tools/business-name-generator`), `WHOIS` (`/domains/whois`) |
| `page_url(path)` | `config.py` | Builds a page URL from `WEB_BASE_URL` and a `PagePath`, e.g. `page_url(PagePath.WHOIS)` |
| `AVAILABILITY_PATH` / `AVAILABILITY_URL` | `config.py` | Public Domain Search API path, kept separate from the web paths |
| `REGISTERED_DOMAIN` | `testdata.py` | Shared test domain (`lotus-music.com`, observed registered during exploration) |

Both base URLs are optional environment overrides; the Production defaults were used for all recorded runs. A maintainability refactor moved these values out of the individual tests; assertions, hydration handling and test logic were not changed, and the full suite gave the same result afterwards (4 passed, 2 skipped, 0 failed).

## 5. Latest Test Execution

**Environment:** Production. **Command:** `python -m pytest -v`. **Result: 4 passed, 2 skipped, 0 failed.**

| Test | Result | Notes |
|---|---|---|
| API: registered domain unavailable | Skipped | `WIX_API_KEY` not configured |
| API: observed response contract | Skipped | `WIX_API_KEY` not configured |
| API: unauthenticated request | Passed | Asserts the **observed** 200; documents behavior, does not verify rejection |
| UI: Storefront search for `lotus-music.com` | Passed | UI says "already registered"; page's availability response has `available = false` |
| UI: WHOIS lookup | Passed | Results page shows registrar REG.RU |
| UI: Business Name Generator | Passed | Names and domain suggestions appear; names vary per run |

Notes on the UI tests:
- Each fills its input only after React hydration (`__react*` element properties). Text filled earlier is discarded by the page, and the search silently does nothing. This workaround relies on frontend internals and is fragile (F-03).
- Initial failures were test-side: the hydration timing, plus a too-strict heading locator in the generator test. They were not confirmed product defects.
- The generator test was run 3 times and passed each time. The other tests were not repeated systematically, so flakiness is not fully assessed.

## 6. Limitations and Remaining Risks

- Payment, charging, registration, renewal and duplicate-purchase scenarios (P0) were **not executed**.
- Authenticated API behavior and UI-vs-public-API consistency are unverified.
- `www.wix.com` and `www.wixapis.com` expose the same availability path; a shared backend is **unverified**.
- Only one registered domain (`lotus-music.com`) was used. Available-domain, premium and invalid-input cases are not automated.
- Mobile, accessibility, cross-browser and AI-quality coverage were not executed.
- `test_whois.py` still contains debug `print` and response-logging lines.

## 7. Quality Strategy (five lines)

1. Prioritize by business risk: money and ownership integrity (P0) before functional coverage (P1) and extended quality (P2).
2. Protect the registration/payment path with idempotency, concurrency and reconciliation tests in a controlled environment.
3. Verify claims against evidence (UI, DevTools network, API) and label them Observed, Documented or Inferred.
4. Keep automation small and stable: contract checks on the API, one happy path per web surface, no sleeps or exact assertions on variable AI output.
5. Report honestly: skipped and not-executed work is stated, and nothing is called a defect without evidence.

## 8. First-Week Ownership Plan

| Day | Focus |
|---|---|
| 1 | Confirm API key and account permissions; unblock the 2 skipped tests; ask owners whether unauthenticated availability is intended (F-01) |
| 2 | Map domain lifecycle and payment flows with service owners; request a staging or sandbox environment and payment simulation |
| 3 | Build P0 tests in staging: idempotent charging, duplicate and concurrent registration, payment-success/registration-failure recovery |
| 4 | Add available-domain, invalid-input and premium-price cases; compare prices and availability across all four surfaces |
| 5 | Run in CI on a schedule with reporting; agree with the frontend team on a stable "ready" signal to replace the `__react*` wait; review findings with the guild |

## 9. Next-Week Improvements

- Replace the hydration workaround with a public readiness signal; add `.env` loading if the team wants it.
- Mobile web (emulation, then real devices), accessibility and cross-browser checks.
- Structured evaluation of generated business names (relevance, safety, multilingual input).
- Monitoring and reconciliation checks for payment-registration consistency.
