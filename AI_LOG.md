# AI_LOG.md — AI Usage and Engineering Review

## 1. AI Tools Used

| Tool | Contribution |
|---|---|
| ChatGPT | Assignment planning, risk prioritization, troubleshooting, review, and drafting of early versions of `FINDINGS.md`, `README.md` and this log |
| Claude Code | Generated `ARCHITECTURE.md` and `TEST_PLAN.md`; implemented the API tests and supporting files (`config.py`, `conftest.py`, `requirements.txt`, `pytest.ini`), plus the later `testdata.py`/`PagePath` refactor; investigated and fixed the UI test failures; wrote the Storefront test; checked why API tests were skipped; updated the final documentation |
| Playwright Codegen | Recording of UI interactions and locator discovery |

The human engineer supplied observed DevTools evidence, reviewed generated output, ran tests, and decided scope and priorities.

## 2. What Claude Code Did, Step by Step

| Step | AI action | Outcome |
|---|---|---|
| Architecture | Wrote `ARCHITECTURE.md` from supplied DevTools observations | Observed/Documented/Inferred separation, Mermaid diagrams |
| Test plan | Wrote `TEST_PLAN.md` | 16 scenarios, P0/P1/P2, exclusions |
| API tests | Implemented 3 tests; ran them without a key | 2 skipped; the unauthenticated test failed against an assumed 401/403 |
| Business Name Generator test | Debugged with Playwright polling scripts | Cause: input value wiped at ~1.0s by hydration; second cause: wrong heading locator |
| WHOIS test | Applied the same diagnosis | Search never navigated before hydration; passes after the wait. Then replaced a 5s sleep with a URL assertion |
| Storefront test | Inspected DOM and network, wrote the test | Passes; asserts UI text and the page's availability response |
| Skipped API tests | Read `conftest.py` and checked for `.env` support | Key read only from the environment; no `.env` loading; tests left skipped |
| Refactor | Moved repeated values into shared helpers (below) | Full suite unchanged: 4 passed, 2 skipped, 0 failed |
| Documentation | Updated the five markdown files, then the README and this log for the refactor | This update |

### Configuration and Test-Data Refactor

- **Why requested:** the domain `lotus-music.com` and the page URLs were hardcoded in several tests. The goal was easier maintenance and readiness for other environments, with no change in test behavior.
- **What Claude Code changed:**
  - Created `testdata.py` with `REGISTERED_DOMAIN`.
  - In `config.py`, added `WEB_BASE_URL` (env `WIX_WEB_BASE_URL`, Production default), a `PagePath` enum (Storefront, Business Name Generator, WHOIS) and a `page_url()` helper. The existing `WIX_API_BASE_URL` override and the API path stay in `config.py`.
  - Updated the three UI tests and the API test to use them.
- **Not changed:** assertions, hydration handling and test logic. The Storefront test's `"check-domain-availability"` response filter was left as a literal substring.
- **Result:** full suite ran after the change: 4 passed, 2 skipped, 0 failed, matching the earlier result.
- **Human review:** Claude Code ran the suite; the diff should still be reviewed by a human before submission.

## 3. Key Prompts (shortened)

- *Architecture:* "Create ARCHITECTURE.md… Do not invent internal service names, databases, or AI model implementations… Do not claim the web endpoints and public API share the same backend without evidence."
- *Test plan:* "Do not fabricate results, internal implementation details, API behavior or defects."
- *API automation:* "Do not change assertions merely to force tests to pass… Skip authenticated tests clearly if the key is absent."
- *UI debugging:* "Diagnose the actual cause using Playwright debugging and browser evidence. Do not assume it is a Wix product bug."
- *Refactor:* "Do not modify assertions, hydration handling, or test logic… If anything fails, restore the previously working behavior."
- *Final documentation:* "Do not invent defects, evidence, execution counts or timing."

## 4. Where AI Was Wrong — and How It Was Caught

| Issue | How it was caught | Resolution |
|---|---|---|
| Claude Code assumed a request without `Authorization` would return 401/403 | It ran the test and got HTTP 200; a direct request confirmed it | Recorded as an observation (F-01), not a vulnerability. The test was later revised to assert the observed 200 |
| Generator test asserted the exact heading "Choose a business name" | Test failed after navigation; page inspection showed "Choose a business name that fits your vision" | Changed the locator to a partial match |
| The Storefront probe used `get_by_role("textbox")` | The element vanished after ~1.5s; its role had become `searchbox` | Switched to the `searchbox` role |
| Early WHOIS failure was logged as "root cause unconfirmed" | Later debugging showed the search never ran because the text was filled before hydration | Hydration wait added; the finding was reclassified as automation timing |
| ChatGPT initially overlooked the dedicated AI log and some README requirements | The assignment instructions were re-read | Missing documents were added |

None of these was treated as a confirmed Wix defect.

## 5. What Was Verified by a Human

- Manual exploration of the four surfaces and the DevTools evidence used in `ARCHITECTURE.md`.
- The manual API request with a key (reported as `400 INVALID_TARGET_ACCOUNT_ID`) and its interpretation. Claude Code never saw or handled the key value.
- Execution of the pytest suite and review of results.
- Decisions on what counts as a defect, and the exclusion of purchases, payments and registrations.
- Final responsibility for repository contents and submission.

Verified by running code (Claude Code's own runs): the hydration timing (value 76 characters at 0.5s, 0 at 1.0s; `__react*` properties appear at ~1.1s), the Storefront availability request and response, and the test results. A human should re-run these before relying on them.

## 6. Changed, Rejected or Deferred

| Item | Action | Reason |
|---|---|---|
| Weakening the missing-auth assertion to pass | Rejected | Would hide the behavior; the 200 was reported instead |
| Arbitrary sleeps as a fix | Rejected | Used an event-based hydration wait; replaced the WHOIS 5s sleep with a URL assertion |
| Confirmed-bug classification | Rejected | Evidence insufficient (F-01, F-02, F-03) |
| Adding `.env` loading | Deferred | Needs a new dependency; not requested |
| Allure, mobile, accessibility, payment scenarios | Deferred / excluded | Timebox and Production safety |

## 7. Final Test Results

`python -m pytest`: 4 passed, 2 skipped, 0 failed.

| Status | Count | Tests |
|---|---:|---|
| Passed | 4 | Unauthenticated API; Storefront UI; WHOIS UI; Business Name Generator UI |
| Skipped | 2 | Authenticated API tests (`WIX_API_KEY` not configured) |
| Failed | 0 | — |

The passing unauthenticated API test asserts the observed 200. It documents behavior and does not prove correct authentication behavior.

## 8. Limitations and Disclosure

- The UI tests depend on a `__react*` readiness workaround, which is fragile.
- Authenticated API behavior is unverified; payment and registration scenarios were not executed.
- Only one registered domain was used. Flakiness was checked for the generator test only (3 of 3 passed).
- No agent configuration files (`CLAUDE.md`, `AGENTS.md`) were used. No personal passwords or API key values were intentionally given to any AI tool.
- Total time spent: `[PLACEHOLDER: total time]`.

## 9. Engineering Ownership

AI sped up implementation and documentation. It did not replace engineering judgment. Each artifact was checked against real browser behavior, API responses and pytest runs, and unverified assumptions are disclosed.
