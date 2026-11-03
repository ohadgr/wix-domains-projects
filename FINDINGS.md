# Findings — Wix Domains

**Environment:** Production (public surfaces only). No purchase, payment or registration was performed.
**Method:** Manual Chrome DevTools exploration plus automated pytest/Playwright checks.
**Final automated result:** 4 passed, 2 skipped, 0 failed.

Classification key: **Observation** (verified behavior, impact unclear), **Potential defect** (behavior likely wrong, needs owner confirmation), **Risk** (unverified exposure), **Blocker** (prevents testing). No finding below is a confirmed product defect.

| ID | Title | Severity | Priority | Classification |
|---|---|---|---|---|
| F-01 | Availability endpoint answers without Authorization | Undetermined | P1 | Observation / needs clarification |
| F-02 | Authenticated API calls blocked by account context | Undetermined | P1 | Blocker (configuration) |
| F-03 | Inputs discard text typed before hydration (~1s) | Low | P2 | Potential defect (UX), partly test-fragility |
| F-04 | Storefront UI and its availability response agree | None | P3 | Observation (positive) |
| F-05 | Payment and registration integrity not validated | Undetermined | P0 (planned) | Risk (Not Executed) |

Severity is the demonstrated impact. Priority is the urgency of follow-up.

## F-01 — Availability endpoint answers without Authorization

- **Surface:** Public Domain Search API (`www.wixapis.com`).
- **Observed:** `GET /domain-search/v2/check-domain-availability?domain=lotus-music.com` with no `Authorization` header returned HTTP 200 and `availability.available = false`, `premium = false`, `premiumType = UNKNOWN_PREMIUM_TYPE`. Repeated with `curl` and `requests`.
- **Documented:** the API reference states an account-level API key is required.
- **Expected (per docs):** an authentication rejection.
- **Evidence:** `tests/api/test_domain_availability.py::test_unauthenticated_availability_response` (passes; it asserts the observed 200, so it documents behavior and does **not** verify rejection).
- **Assessment:** availability data is also shown publicly on the Storefront, so exposure may be low. The endpoint may be intentionally public, or the docs may be out of date. This is not claimed as a vulnerability. Owner confirmation is needed.

## F-02 — Authenticated API calls blocked by account context

- **Surface:** Public Domain Search API.
- **Reported by the tester (manual run, not part of the automated suite):** a request with the available API key returned HTTP 400 `INVALID_TARGET_ACCOUNT_ID`.
- **Automated state:** the two authenticated tests are **skipped** because `WIX_API_KEY` is not set in the test environment. The project does not load `.env` files automatically; the variable must be exported in the shell.
- **Assessment:** an account, key or permission configuration issue is suspected. Not a product defect. API permissions remain unverified.

## F-03 — Inputs discard text typed before client-side hydration

- **Surfaces:** Business Name Generator and WHOIS (value loss verified); Storefront (search had no effect before hydration, and the input role changes from `textbox` to `searchbox` after ~1.5s).
- **Observed (Business Name Generator):** `fill()` succeeded, then the textarea value became empty at about 1.0s with or without pressing Tab. Polling showed `__react*` properties appearing on the element at about 1.1s. After waiting for them, the value persisted and the search worked.
- **Impact:** a user typing within the first second after the field appears (more likely on slow devices) could lose input. Whether real users hit this was not tested. This is inferred, not verified.
- **Test impact:** the three UI tests wait for `__react*` properties before filling. That relies on React internals, may break if Wix changes its frontend, and no public ready signal was found. Initial automation failures were caused by this timing, not by product bugs.
- **Evidence:** `tests/ui/test_business_name_generator.py`, `tests/ui/test_whois.py`, `tests/ui/test_domain_storefront.py` (comments at the hydration wait).

## F-04 — Storefront UI and its availability response agree (one domain)

- **Surface:** Domain Storefront.
- **Observed:** searching `lotus-music.com` showed "lotus-music.com is already registered", and the page's own call `GET https://www.wix.com/domain-search/v2/check-domain-availability?domain=lotus-music.com` returned 200 with `available = false`. The call carried no `Authorization` header.
- **Host difference:** the UI uses `www.wix.com`, the public API uses `www.wixapis.com`, and the path is identical. Whether they share a backend is **unverified**. UI/public-API consistency was not compared because the authenticated tests were skipped.
- **Evidence:** `tests/ui/test_domain_storefront.py` (passes). Covers one registered domain only.

## F-05 — Payment and registration integrity not validated

- **Scope:** duplicate charges, payment success with registration failure, duplicate registration, final charge correctness, premium renewal pricing.
- **Status:** **Not Executed.** Production was used with no payment simulation or backend access, and no purchases were made. No defect is claimed.
- **Why it matters:** these are the highest business risks in the test plan (TC-11 to TC-14). They need a controlled environment with provider simulation and reconciliation access.

## Summary

No confirmed product defects. F-01 and F-02 need owner or account clarification. F-03 is a low-severity potential UX issue. Initial UI test failures were traced to automation timing and a wrong locator, not to product bugs.
