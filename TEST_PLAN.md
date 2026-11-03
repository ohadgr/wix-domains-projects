
# Wix Domains – Test Plan

Evidence baseline: `ARCHITECTURE.md`.

Evidence labels:
- **Observed:** Verified in UI or browser DevTools.
- **Documented:** Described in official Wix documentation.
- **Inferred:** A hypothesis requiring verification.

No internal backend architecture, test results or defects are assumed.

## 1. Objectives and Scope

| Surface | URL |
|---|---|
| Domain Storefront | https://www.wix.com/domains |
| WHOIS Lookup | https://www.wix.com/domains/whois |
| Business Name Generator | https://www.wix.com/tools/business-name-generator |
| Public Domain Search API | https://dev.wix.com/docs/api-reference/account-level/domains/domain-search/introduction |

### Quality Objectives

- **Availability and registration integrity:** Prevent duplicate domain sales and revalidate availability before registration.
- **Pricing and charging:** Ensure the final charge matches the applicable price, currency, taxes, discounts and promotion eligibility.
- **WHOIS:** Validate registration data accuracy and legitimate privacy redaction.
- **Suggestions and TLDs:** Validate suggestion structure, uniqueness and supported TLDs.
- **Business Name Generator:** Validate output relevance and the selected-name-to-domain handoff.
- **Public API:** Validate response contracts, authentication and error handling.
- **Domain lifecycle:** Cover renewal, transfer, expiration and DNS behavior.

The strategy has two levels:

1. **Production Quality Strategy:** Comprehensive risk-based testing for long-term ownership.
2. **Three-Hour Assignment Execution:** A realistic subset implemented and executed within the timebox.

## 2. Production Risk-Based Quality Strategy

Prioritization considers business impact, failure likelihood, integration complexity, customer exposure and production risk.

**Severity vs. Priority**

- **Severity:** The demonstrated impact of an actual defect.
- **Priority:** The urgency of addressing a defect or executing a test.

Production defects generally require faster triage, but severity depends on demonstrated impact rather than environment alone.

| Tier | Key Risks | Assignment Status |
|---|---|---|
| **P0 – Critical business** | Registered domain sold twice; availability revalidated at registration; concurrent registration safety; duplicate charges after retries/timeouts; payment-registration mismatch; recovery, reconciliation or refund; final charged amount correctness; premium registration vs. renewal pricing | **Not Executed** |
| **P1 – Core functional and integration** | API availability, response contract, authentication and safe negative tests; Storefront availability; WHOIS data and redaction; generator output and handoff; suggestions, pagination, TLDs, pricing, promotions and cross-surface consistency | **Primary execution focus** |
| **P2 – Extended** | Mobile web; accessibility; cross-browser and tablet compatibility; AI-generated content quality; resilience and error states; domain lifecycle; observability and monitoring | **Not Executed** |

### P0 – Business-Critical Scenarios

- A registered domain must not be sold twice.
- Domain availability must be revalidated immediately before registration.
- Concurrent registration attempts must preserve registration uniqueness.
- Payment retries and timeouts must not cause duplicate charges.
- Successful payment followed by registration failure must trigger controlled recovery, reconciliation or refund.
- Failed registration must not leave an unresolved customer charge.
- The final charge must match the applicable price, currency, taxes, discounts and promotion eligibility.
- Premium domain registration and renewal prices must be distinguished correctly.

These scenarios are **Not Executed** because the assignment uses public Production environments without controlled payment simulation, transaction access or backend/database validation.

### P1 – Core Functional Coverage

- Public API: registered and dynamically selected available-domain candidates.
- API contract: required fields, types and documented response behavior.
- Authentication: valid key and safe negative cases.
- Invalid domain syntax and unsupported TLD handling.
- Storefront: availability status and consistency with network responses.
- WHOIS: registrar, dates, nameservers, status and privacy redaction.
- Business Name Generator: relevant names and selected-name handoff.
- Domain suggestions: structure, pagination, duplicates and availability.
- Supported TLDs, prices, promotions and geographic context.
- Premium domains when suitable test data is available.

### P2 – Extended Coverage

**Mobile Web**
- Responsive layouts on common mobile viewport sizes.
- Domain search, WHOIS and Business Name Generator usability.
- Touch interactions, scrolling and virtual keyboard behavior.
- Pricing and promotional information visibility on small screens.
- Mobile Safari on iOS and Chrome on Android.
- Playwright device emulation for selected responsive scenarios.
- Real-device testing for browser-specific behavior.

Playwright emulation does not replace testing on physical mobile devices.

**Accessibility and Compatibility**
- Keyboard navigation, focus visibility and semantic labels.
- Screen-reader compatibility and color contrast.
- Cross-browser and tablet behavior.

**AI Quality**
- Generated-name relevance, uniqueness and output structure.
- Unsafe or inappropriate output.
- Multilingual and unusual descriptions.
- Stability of the business-name-to-domain handoff.
- Human review for subjective quality.

**Reliability and Lifecycle**
- Timeouts, retries and graceful error handling.
- Domain renewal, transfer, expiration and DNS propagation.
- Logging, tracing, metrics and payment-registration reconciliation.

P2 scenarios are deliberately excluded from the three-hour execution scope.

## 3. Three-Hour Assignment Execution Plan

**Timebox:** First Git commit at 11:07; final commit before 14:07 Israel time.

The following is an indicative allocation across the entire assignment, not a record of actual time spent.

| Activity | Budget |
|---|---:|
| Setup and architecture exploration | 45 min |
| Test planning | 30 min |
| Findings and exploratory validation | 25 min |
| API and UI automation | 65 min |
| README, AI log, review and final commit | 15 min |
| **Total** | **180 min** |

### Execution Priorities

1. Implement and execute Public Domain Search API tests.
2. Automate at least one web-door UI happy path using Playwright.
3. Record evidence-based findings and exploratory observations.
4. Add optional coverage only if time remains.

The assignment execution subset does not attempt to validate all production-level P0 risks.

## 4. Test Approach and Layers

| Layer | Approach |
|---|---|
| **API** | Python + pytest. Positive availability, response contract validation and a small number of safe negative tests. |
| **UI** | Playwright + pytest. At least one web-door happy path using stable locators and web-first assertions. |
| **Integration** | Compare availability across surfaces within a short window. Validate name-to-domain handoff and equivalent pricing conditions. |
| **Exploratory** | DevTools Network inspection, UI-to-network mapping and evidence-based findings. |
| **AI Quality** | Structural assertions for variable output; human judgment for subjective relevance. |

### API Testing Principles

- Do not assume domain availability remains static.
- Validate response bodies, not HTTP status alone.
- Use documented API contracts.
- Avoid unnecessary or unsafe negative requests.
- Keep request volume low.

### UI Testing Principles

- Prefer user-visible behavior over implementation-specific selectors.
- Use Playwright locator assertions and automatic waiting.
- Avoid arbitrary sleeps.
- Do not assert exact AI-generated names.
- Do not complete purchases or registration flows.

## 5. Test Matrix

### Execution Status Definitions

- **Planned:** Selected for execution but not yet run.
- **Executed / Passed:** Actually executed and passed.
- **Executed / Failed:** Actually executed and failed.
- **Not Executed:** Deliberately excluded from the assignment.
- **Blocked:** Execution attempted but prevented by a documented limitation.

All statuses below reflect the planning stage and must be updated after actual execution.

| ID | Surface / Flow | Scenario | Priority | Layer | Status |
|---|---|---|---|---|---|
| TC-01 | Public API | Registered domain (`lotus-music.com`) reports unavailable | P1 | API | Planned |
| TC-02 | Public API | Dynamic candidate returns valid availability data | P1 | API | Planned |
| TC-03 | Public API | Response matches documented contract | P1 | API | Planned |
| TC-04 | Public API | Invalid domain syntax returns a controlled error | P1 | API | Planned |
| TC-05 | Public API | Missing or invalid credentials are rejected | P1 | API | Planned |
| TC-06 | Storefront | Domain search displays availability status | P1 | UI | Planned |
| TC-07 | WHOIS | Lookup displays registration metadata and handles redaction | P1 | UI / Exploratory | Planned |
| TC-08 | Business Name Generator | Description generates names; selection leads to related domains | P1 | Exploratory | Planned |
| TC-09 | Cross-surface | Availability agrees across Storefront, WHOIS and Public API | P1 | Integration | Planned |
| TC-10 | Suggestions and Pricing | Suggestion structure, pagination, duplicates and supported TLD pricing | P1 | Exploratory / API | Planned |
| TC-11 | Charging | Retries/timeouts do not cause duplicate charges | P0 | Integration | Not Executed |
| TC-12 | Payment and Registration | Registration failure after payment triggers recovery or refund | P0 | Integration | Not Executed |
| TC-13 | Registration | Concurrent or repeat registration of the same domain is prevented | P0 | Integration | Not Executed |
| TC-14 | Premium Pricing | Registration and renewal prices are distinguished | P0 | Integration | Not Executed |
| TC-15 | Domain Lifecycle | Renewal, transfer, expiration and DNS behavior | P2 | Manual / Integration | Not Executed |
| TC-16 | Mobile Web | Responsive layout, touch, keyboard and price visibility | P2 | UI / Mobile Web | Not Executed |

Manual DevTools observations in `ARCHITECTURE.md` are exploratory evidence, not automated test passes.

Public API positive tests may become **Blocked** if the account-level API key lacks the required permissions. Missing-credentials negative testing can be executed independently, subject to Production safety.

## 6. Test Data and Environment Strategy

### Environments

**Actual execution:** Public Production URLs only.

**Design readiness:** Dev, Staging and Production through configurable base URLs or environment settings.

No working non-production URLs are assumed or invented.

Production is treated as a shared environment with real users and transactions. Destructive scenarios require controlled test environments.

### Test Data

| Data | Strategy |
|---|---|
| Registered domain | `lotus-music.com`, observed registered during exploration; revalidate before use |
| Available domains | Dynamically selected and rechecked; availability may change |
| Premium domains | Require verified suitable test data; otherwise excluded |
| WHOIS | Accept legitimate privacy redaction |
| Business Name Generator | Realistic music-store description |
| Generated names | Variable output; avoid exact-name assertions |
| Pricing | Consider currency, geography, taxes, registration period and promotions |

Internal web endpoints and the Public Domain Search API are not assumed to share the same backend.

## 7. Automation Design

### Proposed Project Structure

```text
tests/
  api/
  ui/
conftest.py
config.py
requirements.txt
pytest.ini
```

### Design Principles

- Python, pytest and Playwright.
- Reusable fixtures for API configuration and browser interactions.
- Centralized base URLs and endpoint definitions.
- Environment variables for API keys and credentials.
- No hardcoded secrets or sensitive headers in logs.
- Clear assertions and failure messages.
- Minimal dependencies and maintainable test structure.
- One documented command to run the suite.

Standard pytest output is sufficient for the assignment.

Allure reporting is optional and must not delay core deliverables.

## 8. Exclusions, Blockers and Exit Criteria

### Production Safety

- No purchases, real payments or domain registrations.
- No ownership changes, renewal or transfer operations.
- No load testing, brute force or scraping.
- No intentional rate-limit triggering.
- Low API request volume.
- Public surfaces and the tester's own account only.
- No personal credentials in code or AI prompts.

### Not Executed

- Checkout completion and charging.
- Domain registration and duplicate-purchase scenarios.
- Renewal, transfer, expiration and DNS changes.
- Database and payment-provider reconciliation.
- Mobile real-device testing and full mobile compatibility coverage.
- Full accessibility and cross-browser audits.
- Performance and stress testing.

### Potential Blockers

- Public API permissions or authentication.
- Authenticated UI flows requiring login.

If a blocker occurs, record the exact reason and available evidence. Blocked tests must never be reported as passed.

### Exit Criteria

- Four surfaces mapped in `ARCHITECTURE.md`.
- Risk-based `TEST_PLAN.md` completed.
- `FINDINGS.md` contains up to five evidence-based defects, observations or risks, clearly labeled.
- Public API automation implemented and executed where permissions allow.
- At least one web-door UI test implemented and run.
- Actual results and blockers documented honestly.
- README contains a single test command, total time spent, five-line quality strategy and next-week improvements.
- AI usage, corrections and limitations recorded in `AI_LOG.md`.
- No secrets committed.
- Final Git commit completed before 14:07 Israel time.

If API execution is blocked, preserve the runnable implementation and document the limitation accurately.

The goal is to demonstrate risk awareness, practical automation and transparent reporting rather than claim exhaustive coverage.
