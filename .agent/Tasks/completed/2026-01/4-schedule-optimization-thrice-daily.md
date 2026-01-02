# Task 4 - Thrice-Daily Schedule Optimization ✅

**Completed**: 2026-01-02

## What Was Done
Optimized the news delivery schedule to provide fresh updates three times a day (6:00 AM, 12:00 PM, and 6:00 PM Mountain Time). Implemented dynamic lookback windows to ensure each digest only contains articles published since the previous delivery.

## Key Changes
- **Dynamic Lookback**: Implemented 12-hour window for morning and 6-hour windows for noon/evening digests.
- **Thrice-Daily Schedule**: Added 'noon' digest type and updated crons/workflows for the new intervals.
- **Timezone Alignment**: Migrated all timing logic to `America/Denver` (Mountain Time).

## Notes
- Logic was updated in both `src/aggregator.py` and `.github/workflows/digest.yml` before being migrated to server-side crons.
