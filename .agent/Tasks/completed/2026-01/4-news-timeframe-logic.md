# Task 4 - News Timeframe and Content Logic ✅

**Completed**: 2026-01-06

## What Was Done
Standardized internal time comparisons to UTC and aligned article lookback windows with the requested 6 AM / 12 PM / 6 PM schedule. Added support for the "Noon" digest label.

## Key Changes
- **UTC Standardization**: Replaced `datetime.now()` with `datetime.utcnow()` for all article dates and filter cutoffs to prevent timezone-based article exclusion.
- **Improved Filter Windows**: Morning digest now uses 12h window; Noon and Evening use 6h windows, ensuring no article overlap or gaps.
- **Labeling Support**: Added "Noon" to the digest naming dictionary for both email subjects and headers.

## Notes
- Verified that Josh Allen search results are correctly included in all digests by standardizing API-derived dates to UTC.
