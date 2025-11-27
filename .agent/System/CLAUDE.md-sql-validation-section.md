# CLAUDE.md Template Section: SQL Validation Rules

**Purpose:** Template section for project CLAUDE.md files to enforce SQL validation workflow

**When to Use:** Include this section in any project that uses a Supabase database

**Location in CLAUDE.md:** After "Database Queries" or "Database Configuration" section

---

## Template (Copy to Project CLAUDE.md)

```markdown
## SQL Query Generation Rules ⚠️ MANDATORY

**CRITICAL: All agents MUST follow SQL validation workflow before writing queries**

**See:** [.agent/SOPs/database-sql-validation.md](.agent/SOPs/database-sql-validation.md) for complete workflow

### Quick Reference Rules

**When generating ANY SQL queries:**

1. ✅ **Query schema FIRST** - Use Supabase MCP to introspect actual table structure
   ```sql
   SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_schema = '{YOUR_SCHEMA}' AND table_name = '{TABLE}';
   ```

2. ✅ **Write SQL using EXACT column names** - Cross-reference every column against schema
   ```sql
   -- ✅ CORRECT (validated)
   SELECT {actual_column}, {another_column} FROM {schema}.{table};

   -- ❌ WRONG (guessed)
   SELECT assumed_column FROM table;
   ```

3. ✅ **Validate with EXPLAIN** - Test SQL before returning to user
   ```sql
   EXPLAIN SELECT * FROM {schema}.{table} WHERE {column} > '{value}'::{type};
   ```

4. ✅ **Include validation notes** - Document what was checked
   ```markdown
   **Schema Validation:**
   - ✅ Column `{name}` confirmed ({type} type, NOT "{wrong_guess}")
   - ✅ EXPLAIN succeeded (query is syntactically valid)
   ```

### Common Mistakes to NEVER Make

- ❌ Guessing column names ("date" vs "transaction_date")
- ❌ Missing type casting (`WHERE date > '2025-01-01'` → need `::date`)
- ❌ Forgetting schema prefix (use `{schema}.{table}` NOT just `{table}`)
- ❌ Wrong FK columns (check schema for actual FK column names)
- ❌ Violating NOT NULL constraints (query schema to see required columns)

### Zero Tolerance Policy

**NEVER write SQL without:**
1. Querying live schema via MCP
2. Validating with EXPLAIN
3. Including schema validation notes

**Why this matters:** Prevents 3-4 rounds of error correction, SQL works on first try 95% of time

---

### Example Validated Queries

**{Example 1: Common query for this project}**
```sql
SELECT
  {column1},  -- Confirmed: {type} type (NOT "{wrong_name}")
  {column2},  -- Confirmed: {type} type
  {column3}
FROM {schema}.{table}  -- Explicit schema prefix
WHERE {column1} > '{value}'::{type}  -- Proper type casting
ORDER BY {column1} DESC
LIMIT 10;
```

**Schema Validation:**
- ✅ Column `{column1}` confirmed ({type} type)
- ✅ Schema prefix `{schema}` included
- ✅ EXPLAIN succeeded

---

**{Example 2: JOIN query for this project}**
```sql
SELECT
  a.{column},
  b.{column}
FROM {schema}.{table_a} a
JOIN {schema}.{table_b} b
  ON a.{fk_column} = b.{id};  -- Confirmed: FK is {fk_column}
```

**Schema Validation:**
- ✅ FK `{fk_column}` confirmed ({type}, references {table_b}.{id})
- ✅ EXPLAIN succeeded
```

---

## Customization Instructions

When copying this template to a project CLAUDE.md:

1. **Replace placeholders:**
   - `{YOUR_SCHEMA}` → Your project's schema name (`bookkeeping`, `public`, etc.)
   - `{schema}` → Same schema name in examples
   - `{table}`, `{column}` → Actual table/column names from your project

2. **Add project-specific examples:**
   - Replace example queries with actual common queries for your project
   - Use real table names, column names, and data types
   - Show actual validation notes based on your schema

3. **Reference project SOP:**
   - Update link to point to your project's `database-sql-validation.md`
   - If you only use global SOP, link to `~/Documents/AI_Automation/.agent/SOPs/database-sql-validation-global.md`

4. **Add project context:**
   - Note which tables are most commonly queried
   - Document any unusual column naming patterns
   - List common data types (uuid, date, numeric, etc.)

---

## Example: Customized for expense-tracker Project

```markdown
## SQL Query Generation Rules ⚠️ MANDATORY

**CRITICAL: All agents MUST follow SQL validation workflow before writing queries**

**See:** [.agent/SOPs/database-sql-validation.md](.agent/SOPs/database-sql-validation.md) for complete workflow

### Quick Reference Rules

**When generating ANY SQL queries:**

1. ✅ **Query schema FIRST** - Use Supabase MCP to introspect actual table structure
   ```sql
   SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_schema = 'bookkeeping' AND table_name = '{TABLE}';
   ```

2. ✅ **Write SQL using EXACT column names** - Cross-reference every column against schema
   ```sql
   -- ✅ CORRECT (validated)
   SELECT transaction_date, amount FROM bookkeeping.transactions;

   -- ❌ WRONG (guessed)
   SELECT date, value FROM transactions;
   ```

3. ✅ **Validate with EXPLAIN** - Test SQL before returning to user
   ```sql
   EXPLAIN SELECT * FROM bookkeeping.transactions WHERE transaction_date > '2025-01-01'::date;
   ```

4. ✅ **Include validation notes** - Document what was checked
   ```markdown
   **Schema Validation:**
   - ✅ Column `transaction_date` confirmed (date type, NOT "date")
   - ✅ EXPLAIN succeeded (query is syntactically valid)
   ```

### Common Mistakes to NEVER Make

- ❌ Guessing column names ("date" vs "transaction_date")
- ❌ Missing type casting (`WHERE date > '2025-01-01'` → need `::date`)
- ❌ Forgetting schema prefix (use `bookkeeping.transactions` NOT just `transactions`)
- ❌ Wrong FK columns (check schema for actual FK column names)
- ❌ Violating NOT NULL constraints (query schema to see required columns)

### Zero Tolerance Policy

**NEVER write SQL without:**
1. Querying live schema via MCP
2. Validating with EXPLAIN
3. Including schema validation notes

**Why this matters:** Prevents 3-4 rounds of error correction, SQL works on first try 95% of time

---

### Example Validated Queries

**Get transactions from last month:**
```sql
SELECT
  id,
  transaction_date,  -- Confirmed: date type (NOT "date")
  amount,            -- Confirmed: numeric type
  description
FROM bookkeeping.transactions  -- Explicit schema prefix
WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY transaction_date DESC
LIMIT 10;
```

**Schema Validation:**
- ✅ Column `transaction_date` confirmed (date type)
- ✅ Schema prefix `bookkeeping` included
- ✅ EXPLAIN succeeded

---

**Get account balance with type:**
```sql
SELECT
  a.account_name,
  a.current_balance,  -- Confirmed: NOT "balance"
  at.type_name
FROM bookkeeping.accounts a
JOIN bookkeeping.account_types at
  ON a.account_type_id = at.id;  -- Confirmed: FK is account_type_id
```

**Schema Validation:**
- ✅ Column `current_balance` confirmed (NOT "balance")
- ✅ FK `account_type_id` confirmed (integer, references account_types.id)
- ✅ EXPLAIN succeeded
```

---

## Integration with agent-structure Skill

**When agent-structure skill creates .agent/ folder for new projects:**

1. Check if project uses Supabase database
   - Look for Supabase MCP in proposed `.claude/config.json`
   - Check if database mentioned in project description

2. If database detected:
   - Create `.agent/SOPs/database-sql-validation.md` (copy from global SOP)
   - Add SQL validation section to project CLAUDE.md (use this template)
   - Customize examples based on project schema name

3. Remind user to:
   - Configure Supabase MCP server
   - Update schema name in templates
   - Add project-specific query examples

---

## Adoption Checklist

**When adding SQL validation to existing project:**

- [ ] Verify Supabase MCP is configured (`.claude/config.json`)
- [ ] Determine project schema name (query database or check docs)
- [ ] Copy this template section to project CLAUDE.md
- [ ] Replace `{YOUR_SCHEMA}` with actual schema name
- [ ] Create/reference project SQL validation SOP
- [ ] Add 2-3 project-specific validated query examples
- [ ] Test with sample SQL generation
- [ ] Document common tables and columns in examples

---

**Template Version:** 1.0
**Created:** 2025-11-18
**Last Updated:** 2025-11-18
