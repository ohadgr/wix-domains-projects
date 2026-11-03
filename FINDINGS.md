# Findings — Wix Domains

**Environment:** Production  
**Test approach:** Manual exploration using Chrome DevTools and automated checks using Python, pytest and Playwright.

## F-01 — WHOIS search results not verified in automated execution

- **Severity:** Undetermined
- **Priority:** P2 — Investigation
- **Status:** Automation failure; product defect not confirmed
- **Surface:** WHOIS Lookup

### Steps to Reproduce
1. Navigate to `https://www.wix.com/domains/whois`.
2. Enter `lotus-music.com`.
3. Click **Search Domains**.
4. Wait for the WHOIS results.

### Expected Result
The search displays registration information for the requested domain, including registrar details.

### Actual Result
The Playwright execution did not locate the expected registrar value `REG.RU`. The test failed on the result assertion.

### Evidence
- `tests/ui/test_whois.py`
- pytest failure: `Locator expected to be visible`
- Manual exploration previously observed WHOIS information for this domain.

### Assessment
The root cause remains unconfirmed. Possible explanations include an automation synchronization issue, navigation behavior or a product issue. This is not classified as a confirmed product defect.

## F-02 — Domain Search API account context unresolved

- **Severity:** Undetermined
- **Priority:** P1 — Investigation
- **Status:** Integration/configuration issue suspected; product defect not confirmed
- **Surface:** Public Domain Search API

### Steps to Reproduce
1. Send a domain availability request to the public Domain Search API.
2. Include the configured API key in the `Authorization` header.
3. Observe the response.

### Expected Result
An authenticated request with all required account context returns domain availability information.

### Actual Result
The authenticated request returned HTTP `400` with error code `INVALID_TARGET_ACCOUNT_ID`. A separate request without the Authorization header returned HTTP `200` with availability information.

### Evidence
- `tests/api/test_domain_availability.py`
- HTTP `400` response containing `INVALID_TARGET_ACCOUNT_ID`
- HTTP `200` unauthenticated response for `lotus-music.com`

### Assessment
The required Wix account context and authentication contract have not been fully verified. The HTTP `200` response without Authorization does not, by itself, establish a security vulnerability.

## Summary

No confirmed product defects are reported from these two observations. Both findings remain open for further investigation. Purchase, payment, registration and duplicate-purchase scenarios were not executed against Production.