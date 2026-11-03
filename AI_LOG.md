# AI_LOG.md — AI Usage and Engineering Review

## 1. AI Tools Used

| Tool | Contribution |
|---|---|
| ChatGPT | (As recorded by the engineer; ChatGPT sessions are not visible in the repository.) Assignment planning, risk prioritization, troubleshooting, review, and drafting of early versions of `FINDINGS.md`, `README.md` and this log |
| Claude Code | Generated `ARCHITECTURE.md` and `TEST_PLAN.md`; implemented the API tests and supporting files (`config.py`, `conftest.py`, `requirements.txt`, `pytest.ini`), plus the later `testdata.py`/`PagePath` refactor; investigated and fixed the UI test failures; wrote the Storefront test; checked why API tests were skipped; updated the final documentation |
| Playwright Codegen | Recording of UI interactions and locator discovery (as recorded by the engineer; not visible in the repository) |

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
| Documentation | Updated the five markdown files, then the README and this log for the refactor | Included in commit `aba37c6` |
| Final cleanup | Updated time statements, statuses and this log; removed debug output from `tests/ui/test_whois.py` | Included in commit `0819f3b` (13:59:43 +0200) |
| WHOIS investigation | Standalone timing checks of the results page; documentation updates | Registrar details load slowly or intermittently; a later timeout change (15000 to 45000 ms) is not part of `0819f3b` |

### Configuration and Test-Data Refactor

- **Why requested:** the domain `lotus-music.com` and the page URLs were hardcoded in several tests. The goal was easier maintenance and readiness for other environments, with no change in test behavior.
- **What Claude Code changed:**
  - Created `testdata.py` with `REGISTERED_DOMAIN`.
  - In `config.py`, added `WEB_BASE_URL` (env `WIX_WEB_BASE_URL`, Production default), a `PagePath` enum (Storefront, Business Name Generator, WHOIS) and a `page_url()` helper. The existing `WIX_API_BASE_URL` override and the API path stay in `config.py`.
  - Updated the three UI tests and the API test to use them.
- **Not changed:** assertions, hydration handling and test logic. The Storefront test's `"check-domain-availability"` response filter was left as a literal substring.
- **Result:** full suite ran after the change: 4 passed, 2 skipped, 0 failed, matching the earlier result.
- **Verification:** Claude Code ran the suite after the change. This log records no separate human review of the refactor diff.

### Cross-Model Review Workflow

- **Roles:** Claude Code handled implementation and debugging. ChatGPT (GPT-6, as stated by the engineer) performed an independent AI-assisted review of Claude Code's pushed GitHub implementation and documentation, identified issues and recommended corrections.
- **Nature of the review:** an informal AI-assisted code review. It was not a formal, scored LLM-as-a-Judge evaluation: there was no scoring rubric, no repeated or calibrated judging, and no measured agreement between models.
- **Limits of ChatGPT's role:** it reviewed the pushed repository content only. It did not execute tests, and none of the recorded test results come from it.
- **Records:** the specific issues it raised and the corrections made are not itemized in this log. The review sessions are not visible in the repository.
- **Responsibility:** the human engineer retained final responsibility. They reviewed the recommendations, decided which to apply and retained final responsibility for the repository and submission.

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
| Claude Code assumed a request without `Authorization` would return 401/403 | It ran the test and got HTTP 200; a direct request confirmed it | Recorded as an observation (F-01), not a vulnerability. The test was later revised to assert the observed 200 (the revision happened outside the Claude Code session recorded here) |
| Generator test asserted the exact heading "Choose a business name" | Test failed after navigation; page inspection showed "Choose a business name that fits your vision" | Changed the locator to a partial match |
| The Storefront probe used `get_by_role("textbox")` | The element vanished after ~1.5s; its role had become `searchbox` | Switched to the `searchbox` role |
| Early WHOIS failure was logged as "root cause unconfirmed" | Later debugging showed the search never ran because the text was filled before hydration | Hydration wait added; the finding was reclassified as automation timing |
| ChatGPT initially overlooked the dedicated AI log and some README requirements | The assignment instructions were re-read | Missing documents were added |

None of these was treated as a confirmed Wix defect.

## 5. What Was Verified by a Human

*As recorded by the engineer; Claude Code cannot independently confirm these.*

- Manual exploration of the four surfaces and the DevTools evidence used in `ARCHITECTURE.md`.
- The manual API request with a key (reported as `400 INVALID_TARGET_ACCOUNT_ID`) and its interpretation. Claude Code never saw or handled the key value.
- Execution of the pytest suite and review of results.
- Decisions on what counts as a defect, and the exclusion of purchases, payments and registrations.
- Final responsibility for repository contents and submission.

Verified by running code (Claude Code's own runs): the hydration timing (value 76 characters at 0.5s, 0 at 1.0s; `__react*` properties appear at ~1.1s), the Storefront availability request and response, and the test results. These were not independently re-run by a human as far as this log can show.

## 6. Changed, Rejected or Deferred

| Item | Action | Reason |
|---|---|---|
| Weakening the missing-auth assertion to pass | Rejected | Would hide the behavior; the 200 was reported instead |
| Arbitrary sleeps as a fix | Rejected | Used an event-based hydration wait; replaced the WHOIS 5s sleep with a URL assertion |
| Confirmed-bug classification | Rejected | Evidence insufficient (F-01, F-02, F-03) |
| Adding `.env` loading | Deferred | Needs a new dependency; not requested |
| Allure | Deferred | Optional; not essential within the timebox |
| Mobile, accessibility, cross-browser, payment and registration scenarios | Not executed | Timebox and Production safety |

## 7. Final Test Results

An earlier full run gave 4 passed, 2 skipped, 0 failed. The **latest full run gave 3 passed, 1 failed, 2 skipped**: the WHOIS test failed because the expected registrar `REG.RU` was absent from the rendered page. WHOIS navigated successfully, but registrar details were still loading. The registrar assertion timeout was then changed from 15000 to 45000 ms and one isolated WHOIS run passed. Full-suite stability after this change has not been verified. WHOIS is documented as potentially flaky and requiring investigation; the root cause is not confirmed and it is not a Wix defect.

| Status | Count | Tests |
|---|---:|---|
| Passed | 3 | Unauthenticated API; Storefront UI; Business Name Generator UI |
| Failed | 1 | WHOIS UI (intermittent; one isolated run passed after the timeout change) |
| Skipped | 2 | Authenticated API tests (`WIX_API_KEY` not configured) |

The passing unauthenticated API test asserts the observed 200. It documents behavior and does not prove correct authentication behavior.

## 8. Limitations and Disclosure

- The UI tests depend on a `__react*` readiness workaround, which is fragile.
- Authenticated API behavior is unverified; payment and registration scenarios were not executed.
- The WHOIS UI test is potentially flaky and needs investigation. It failed in the latest full run and in 2 of 3 isolated runs by Claude Code (after its debug output was removed, which a standalone check showed was not the cause); a standalone check found the registrar data appearing after 9 to 17 seconds and once not within 30 seconds. After the timeout was raised to 45000 ms, one isolated run passed; full-suite stability is unverified. The cause is not established, and it is not a confirmed Wix defect.
- Only one registered domain was used. Flakiness was checked for the generator test only (3 of 3 passed).
- No agent configuration files (`CLAUDE.md`, `AGENTS.md`) were used. No personal passwords or API key values were intentionally given to any AI tool.
- Elapsed time through the previous final commit (`0819f3b`, 13:59:43 +0200): 2h 52m 58s from the first commit (11:06:45 +0200). Any later commit extends this; the deadline is 14:06:45 +0200.

## 9. Engineering Ownership

AI sped up implementation and documentation. Claude Code checked its work against real browser behavior, API responses and pytest runs in its own sessions. Human verification is limited to the items in section 5, and unverified assumptions are disclosed. The submission is not complete until the engineer reviews and makes the final commit.
