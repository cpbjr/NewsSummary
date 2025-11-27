# Timezone Handling Standard Operating Procedure

**User Timezone:** America/Denver (Mountain Time - MST/MDT)
**Last Updated:** 2025-11-27
**Applies To:** All projects with date/time handling

---

## TL;DR - Core Principles

1. ✅ **Store UTC in database** - All timestamps in PostgreSQL as `TIMESTAMPTZ`
2. ✅ **Display in Mountain Time** - Convert to `America/Denver` for user-facing displays
3. ✅ **Centralize timezone logic** - Single source of truth per stack
4. ✅ **Never hard-code timezones** - Use configuration variables
5. ✅ **Test DST transitions** - Verify behavior in March/November

---

## Configuration

### Environment Variable (Backend)

```bash
# .env file
TIMEZONE=America/Denver  # Mountain Time with DST support
```

**Alternative timezones** (if needed):
- `America/Phoenix` - Arizona (no DST)
- `America/Los_Angeles` - Pacific Time
- `America/Chicago` - Central Time
- `America/New_York` - Eastern Time

### Why America/Denver?

- **MST in winter** (UTC-7): November through March
- **MDT in summer** (UTC-6): March through November
- **Auto DST handling** - Library adjusts automatically
- **User location** - Matches Mountain states timezone

---

## Backend Implementation (Python/Flask)

### Setup: Config Class

**File:** `config.py`

```python
import os

class Config:
    # Timezone Configuration
    TIMEZONE = os.getenv('TIMEZONE', 'America/Denver')
```

### ✅ CORRECT Pattern

```python
import pytz
from datetime import datetime
from config import Config

# Get current time in configured timezone
mountain = pytz.timezone(Config.TIMEZONE)
now = datetime.now(mountain)

# For dates only (no time component)
work_date = now.date().isoformat()  # "2025-11-27"

# For timestamps (with timezone)
start_time = now.isoformat()  # "2025-11-27T14:30:00-07:00"
```

### ❌ WRONG Patterns

```python
# ❌ WRONG - Hard-coded timezone
mountain = pytz.timezone('America/Denver')  # Use Config.TIMEZONE instead

# ❌ WRONG - Naive datetime (no timezone)
now = datetime.now()  # No timezone info

# ❌ WRONG - UTC when user expects local time
now = datetime.utcnow()  # User sees wrong time
```

### Database Storage

**Date Fields (DATE type):**
```python
# ✅ Store as simple date string (no timezone conversion)
work_date = now.date().isoformat()  # "2025-11-27"
```

**Timestamp Fields (TIMESTAMPTZ type):**
```python
# ✅ Store as timezone-aware datetime (database converts to UTC)
start_time = now.isoformat()  # "2025-11-27T14:30:00-07:00"
```

**How PostgreSQL TIMESTAMPTZ works:**
1. **Input:** Accepts timezone-aware datetime (`2025-11-27T14:30:00-07:00`)
2. **Storage:** Stores as UTC internally (`2025-11-27T21:30:00Z`)
3. **Output:** Returns in session timezone (default UTC, convert in app layer)

---

## Frontend Implementation (React/TypeScript)

### Setup: Centralized Utility

**File:** `src/lib/timezone.ts`

```typescript
import { format, toZonedTime } from 'date-fns-tz'
import { parseISO } from 'date-fns'

export const MOUNTAIN_TIME = 'America/Denver'

/**
 * Core formatting function - all others use this
 */
export function formatInMountainTime(timestamp: string, formatStr: string): string {
  const date = parseISO(timestamp)
  const mountainTime = toZonedTime(date, MOUNTAIN_TIME)
  return format(mountainTime, formatStr, { timeZone: MOUNTAIN_TIME })
}

/**
 * Format time only (e.g., "3:30 PM")
 */
export function formatTime(timestamp: string): string {
  return formatInMountainTime(timestamp, 'h:mm a')
}

/**
 * Format date only (e.g., "Nov 27, 2025")
 */
export function formatDate(dateString: string): string {
  return formatInMountainTime(dateString, 'MMM dd, yyyy')
}

/**
 * Get current date in Mountain Time for input[type="date"]
 */
export function getCurrentDateForInput(): string {
  const now = new Date()
  const mountainNow = toZonedTime(now, MOUNTAIN_TIME)
  return format(mountainNow, 'yyyy-MM-dd', { timeZone: MOUNTAIN_TIME })
}
```

### ✅ CORRECT Pattern

```typescript
// ✅ CORRECT - Will display Mountain Time
import { formatTime, formatDate } from '@/lib/timezone'

function MyComponent() {
  const timestamp = "2025-11-27T15:30:00+00:00"
  return (
    <div>
      <p>{formatTime(timestamp)}</p>  {/* Shows: "8:30 AM" (MST) */}
      <p>{formatDate(timestamp)}</p>  {/* Shows: "Nov 27, 2025" */}
    </div>
  )
}
```

### ❌ WRONG Patterns

```typescript
// ❌ WRONG - Will display UTC time
import { format, parseISO } from 'date-fns'

function MyComponent() {
  const timestamp = "2025-11-27T15:30:00+00:00"
  return <div>{format(parseISO(timestamp), 'h:mm a')}</div>
  // Shows: "3:30 PM" (UTC) instead of "8:30 AM" (MST) ❌
}

// ❌ WRONG - Browser timezone (unpredictable)
const date = new Date(timestamp).toLocaleDateString('en-US')

// ❌ WRONG - Custom timezone logic in components
const offset = -7 * 60 // Mountain Time offset (DON'T DO THIS)
```

---

## Testing Checklist

When implementing timezone handling:

### Backend (Python)
- [ ] Import `pytz` and `Config`
- [ ] Replace `datetime.utcnow()` with `datetime.now(pytz.timezone(Config.TIMEZONE))`
- [ ] Replace hard-coded `'America/Denver'` with `Config.TIMEZONE`
- [ ] Verify `.env` has `TIMEZONE=America/Denver`
- [ ] Test health check endpoint shows correct timezone
- [ ] Verify date fields use `.date().isoformat()` (not full datetime)

### Frontend (React)
- [ ] Install `date-fns-tz` dependency
- [ ] Create `src/lib/timezone.ts` utility file
- [ ] Import from `@/lib/timezone` (never use `date-fns` directly in components)
- [ ] Test at 12:00 AM (midnight edge case)
- [ ] Test at 11:59 PM (end of day edge case)
- [ ] Test during DST transition weeks (March/November)
- [ ] Verify display shows Mountain Time, not UTC

### Database
- [ ] All timestamp columns use `TIMESTAMPTZ` type
- [ ] Date-only columns use `DATE` type (no timezone conversion)
- [ ] Verify database stores UTC (check raw values)
- [ ] Test queries return expected timezone-aware data

---

## Common Mistakes & Solutions

### Issue: Dates are off by one day

**Symptom:** Transaction shows wrong date in database

**Cause:** Timezone conversion happening when it shouldn't

**Solution:** Use date-only fields for dates (not timestamps)

```python
# ✅ CORRECT - Date fields stay as dates
work_date = now.date().isoformat()  # "2025-11-27"

# ❌ WRONG - Timestamp gets converted
work_date = now.isoformat()  # "2025-11-27T14:30:00-07:00"
```

---

### Issue: Times show UTC instead of Mountain Time

**Symptom:** Health check or logs show UTC time

**Cause:** Using `datetime.utcnow()` instead of configured timezone

**Solution:** Always use `Config.TIMEZONE`

```python
# ✅ CORRECT
mountain = pytz.timezone(Config.TIMEZONE)
now = datetime.now(mountain)

# ❌ WRONG
now = datetime.utcnow()
```

---

### Issue: Frontend shows UTC time

**Symptom:** Time displays are 6-7 hours off

**Cause:** Using `date-fns` directly without timezone conversion

**Solution:** Use centralized utility functions

```typescript
// ✅ CORRECT
import { formatTime } from '@/lib/timezone'
const time = formatTime(timestamp)

// ❌ WRONG
import { format, parseISO } from 'date-fns'
const time = format(parseISO(timestamp), 'h:mm a')
```

---

## DST (Daylight Saving Time) Handling

**When does DST change?**
- **Spring Forward:** 2nd Sunday in March (2:00 AM → 3:00 AM)
- **Fall Back:** 1st Sunday in November (2:00 AM → 1:00 AM)

**How libraries handle DST:**
- ✅ `pytz` (Python) - Automatically adjusts for DST
- ✅ `date-fns-tz` (JavaScript) - Automatically adjusts for DST
- ❌ Manual offset calculation - **NEVER DO THIS** (breaks during DST)

**Testing DST transitions:**
```python
# Test spring forward (March)
test_date = datetime(2025, 3, 9, 2, 30, tzinfo=pytz.timezone('America/Denver'))
# Will show 3:30 AM (skipped 2:00-3:00 AM)

# Test fall back (November)
test_date = datetime(2025, 11, 2, 1, 30, tzinfo=pytz.timezone('America/Denver'))
# Will show 1:30 AM (repeated 1:00-2:00 AM)
```

---

## Migration Checklist

When fixing timezone issues in existing code:

### Backend (Python)
- [ ] Import `pytz` and `Config`
- [ ] Replace `datetime.utcnow()` with `datetime.now(pytz.timezone(Config.TIMEZONE))`
- [ ] Replace hard-coded `'America/Denver'` with `Config.TIMEZONE`
- [ ] Ensure all datetime operations use timezone-aware datetimes
- [ ] Verify `.env` has `TIMEZONE=America/Denver`
- [ ] Deploy and verify health check shows correct timezone

### Frontend (React)
- [ ] Install `date-fns-tz`: `npm install date-fns-tz`
- [ ] Create `src/lib/timezone.ts` utility file
- [ ] Add utility functions: `formatTime`, `formatDate`, `getCurrentDateForInput`
- [ ] Find all `import { format, parseISO } from 'date-fns'` in components
- [ ] Replace with `import { formatTime, formatDate } from '@/lib/timezone'`
- [ ] Test each page with date/time displays
- [ ] Verify input defaults use `getCurrentDateForInput()`

---

## Summary

### Do's ✅

**Backend (Python):**
- ✅ Use `Config.TIMEZONE` for all timezone operations
- ✅ Use timezone-aware datetimes (`datetime.now(pytz.timezone(Config.TIMEZONE))`)
- ✅ Store dates as `YYYY-MM-DD` strings (no timezone conversion)
- ✅ Store timestamps as `TIMESTAMPTZ` (database handles UTC)

**Frontend (React):**
- ✅ Create centralized `@/lib/timezone` utility
- ✅ Import from utility (never use `date-fns` directly)
- ✅ Use `formatTime()`, `formatDate()` for displays
- ✅ Use `getCurrentDateForInput()` for default values

**Database:**
- ✅ Store all timestamps as `TIMESTAMPTZ` (UTC internally)
- ✅ Store dates as `DATE` (no timezone)
- ✅ Convert to Mountain Time in application layer

### Don'ts ❌

**Backend (Python):**
- ❌ Never use `datetime.utcnow()` for user-facing times
- ❌ Never hard-code timezone strings (`'America/Denver'`)
- ❌ Never use naive datetimes (`datetime.now()` without timezone)
- ❌ Never convert date fields to timestamps

**Frontend (React):**
- ❌ Never use `date-fns` format directly in components
- ❌ Never use browser's `toLocaleDateString()` without timezone
- ❌ Never create custom timezone logic in components
- ❌ Never hard-code UTC offset calculations

**Database:**
- ❌ Never store Mountain Time directly in database
- ❌ Never use `TIMESTAMP` (use `TIMESTAMPTZ` instead)
- ❌ Never attempt timezone conversion in SQL queries

---

## Related Documentation

**Project-Specific SOPs:**
- Backend: `.agent/SOPs/timezone-handling-python-bot.md` (if Python backend)
- Frontend: `.agent/SOPs/timezone-standardization.md` (if React frontend)
- Database: Migration files in `supabase/migrations/` (TIMESTAMPTZ usage)

**External References:**
- Python `pytz` docs: https://pypi.org/project/pytz/
- `date-fns-tz` docs: https://date-fns.org/docs/Time-Zones
- IANA timezone list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- PostgreSQL TIMESTAMPTZ: https://www.postgresql.org/docs/current/datatype-datetime.html

---

## Notes

**Created:** 2025-11-27
**Based On:** expense-tracker project timezone standardization (Sessions 51, 66)
**User Timezone:** America/Denver (Mountain Time with DST)

This SOP provides the foundation for consistent timezone handling across all projects. For project-specific implementation details, create a project-specific SOP that references this template.
