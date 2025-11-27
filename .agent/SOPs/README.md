# Standard Operating Procedures (SOPs)

This directory contains project-specific standard operating procedures and workflows.

---

## Purpose

SOPs document:
- **Repeatable processes** - How to perform common tasks correctly
- **Best practices** - Proven patterns that work well
- **Workflow guidelines** - Step-by-step procedures
- **Decision frameworks** - When to use which approach
- **Tool usage** - How to use specific tools or technologies

---

## When to Create SOPs

Create a new SOP when:
- ✅ You discover a **repeatable process** that will be used multiple times
- ✅ There's a **non-obvious solution** that took significant time to figure out
- ✅ You want to **standardize an approach** across the team
- ✅ You need to **document a complex workflow** with multiple steps
- ✅ There are **multiple ways** to do something and you've chosen the best one

**Don't create SOPs for:**
- ❌ One-time tasks
- ❌ Obvious processes (covered in tool documentation)
- ❌ Project-specific implementation details (use Tasks/Implementation/ instead)

---

## SOP Structure Template

```markdown
# {SOP Title}

**Applies to:** {What this applies to}
**Purpose:** {Why this SOP exists}
**Created:** {Date}
**Priority:** {CRITICAL | HIGH | MEDIUM | LOW}

---

## Problem Statement

{What problem does this solve?}

---

## Solution / Workflow

{Step-by-step process}

### Step 1: {Action}
{Details}

### Step 2: {Action}
{Details}

---

## Examples

{Concrete examples showing the SOP in action}

---

## Common Mistakes & How to Avoid Them

- ❌ **Mistake:** {What not to do}
  - ✅ **Fix:** {What to do instead}

---

## Checklist

- [ ] {Required step 1}
- [ ] {Required step 2}

---

## Related Documentation

- {Link to related SOPs or documentation}

---

**Last Updated:** {Date}
```

---

## Common SOPs (Reference Global SOPs)

### Database & SQL

**For projects using Supabase databases:**

Reference the **global SQL validation SOP** in workspace root:
- **Location:** `~/Documents/AI_Automation/.agent/SOPs/database-sql-validation-global.md`
- **Purpose:** Mandatory MCP-first SQL generation to eliminate schema errors
- **Applies to:** ALL SQL query generation

**To adopt in your project:**
1. Create project-specific SOP (optional but recommended):
   ```bash
   cp ~/Documents/AI_Automation/.agent/SOPs/database-sql-validation-global.md \
      database-sql-validation.md
   ```

2. Customize for your project:
   - Schema name (bookkeeping, public, custom)
   - Common tables and queries
   - Project-specific patterns

3. Reference in project CLAUDE.md:
   ```markdown
   ## SQL Query Generation Rules

   **CRITICAL:** Follow [.agent/SOPs/database-sql-validation.md]

   Quick rules:
   1. Query schema FIRST via Supabase MCP
   2. Write SQL using EXACT column names
   3. Validate with EXPLAIN
   4. Include validation notes
   ```

**Why this matters:**
- ✅ SQL works on first try 95% of time (vs 25% without validation)
- ✅ Eliminates 3-4 rounds of error correction per query
- ✅ Saves 8+ minutes per query
- ✅ Zero column name or type mismatch errors

---

### Design & UI

**For projects with visual design workflows:**

See `design-review.md` for visual design validation process.

---

### Deployment & Operations

**For production deployment procedures:**

Create project-specific deployment SOPs:
- Pre-deployment checklist
- Deployment steps
- Rollback procedures
- Post-deployment verification

**Example structure:**
- `deployment-frontend.md` - Frontend deployment workflow
- `deployment-backend.md` - Backend/bot deployment workflow
- `database-migrations.md` - How to safely apply migrations

---

## Organizing SOPs

### Directory Structure

```
SOPs/
├── README.md                          # This file
├── database-sql-validation.md         # SQL generation workflow
├── design-review.md                   # Visual design validation
├── deployment-frontend.md             # Frontend deployment
├── deployment-backend.md              # Backend deployment
├── {technology}/                      # Technology-specific SOPs
│   ├── react-component-patterns.md
│   ├── telegram-bot-workflows.md
│   └── n8n-workflow-patterns.md
└── {process}/                         # Process-specific SOPs
    ├── code-review-checklist.md
    ├── testing-strategy.md
    └── debugging-workflow.md
```

### Naming Conventions

**Good SOP names:**
- `database-sql-validation.md` - Clear, specific
- `react-component-patterns.md` - Technology + topic
- `deployment-frontend.md` - Process + context

**Avoid:**
- `sop-1.md` - Not descriptive
- `notes.md` - Too generic
- `temp.md` - Sounds temporary

---

## SOP Maintenance

### When to Update SOPs

- ✅ Technology/tool version changes significantly
- ✅ Better approach discovered
- ✅ Common mistakes identified
- ✅ Process needs clarification based on team feedback

### Update Checklist

- [ ] Update "Last Updated" date
- [ ] Test procedure still works
- [ ] Update examples if needed
- [ ] Check related documentation links
- [ ] Announce significant changes to team

---

## Integration with Project Documentation

### How SOPs Relate to Other `.agent/` Folders

**SOPs/ (How to do things)**
- Procedures and workflows
- Best practices
- Step-by-step guides

**System/ (Current state)**
- Architecture documentation
- Tech stack details
- Database schema
- Integration points

**Tasks/ (What to do)**
- Work items and features
- Implementation plans
- Task tracking

**Design/ (Visual standards)**
- Design principles
- Style guides
- Component library

---

## Examples from Real Projects

### Expense Tracker
- `database-sql-validation.md` - SQL validation workflow
- `database-budget-sync.md` - Budget calculation procedures
- `how-to-deploy-dashboard.md` - Dashboard deployment
- `ui-design-workflow.md` - Visual design process

### Maintenance Log
- `telegram-bot-deployment.md` - Bot deployment workflow
- `ai-parsing-patterns.md` - How to use AI parser

---

## FAQ

### Q: SOP vs Implementation Plan - What's the Difference?

**SOP (Standard Operating Procedure):**
- **Reusable** process for multiple similar tasks
- **Generic** - applies to many instances
- **Permanent** - stays in SOPs/ folder
- **Example:** "How to deploy any frontend"

**Implementation Plan:**
- **One-time** detailed plan for specific feature
- **Specific** - applies to one task only
- **Temporary** - moves to completed/ when done
- **Example:** "Plan to add photo upload feature"

### Q: When Should I Reference Global SOPs vs Create Project-Specific?

**Reference global SOPs when:**
- Process is universal across projects
- No project-specific customization needed
- Want to stay in sync with workspace standards

**Create project-specific when:**
- Need to customize for project context
- Project has unique requirements
- Want examples specific to your tables/code

**Best approach:** Reference global SOP in project CLAUDE.md + optionally create customized version in project SOPs/

### Q: How Do I Know If My SOP Is Good?

**Good SOP characteristics:**
- ✅ Can be followed by someone unfamiliar with the project
- ✅ Has clear steps (numbered or checkboxes)
- ✅ Includes examples
- ✅ Explains WHY not just WHAT
- ✅ Has checklist for verification
- ✅ Documents common mistakes

---

## Getting Started

**For new projects:**

1. **Check workspace global SOPs** (`~/Documents/AI_Automation/.agent/SOPs/`)
   - Copy/reference relevant ones

2. **Create project-specific SOPs as needed**
   - Start with deployment procedures
   - Add SQL validation if using database
   - Document unique workflows

3. **Reference in CLAUDE.md**
   - Link to critical SOPs
   - Ensure agents know to follow them

4. **Keep updated**
   - Update as processes evolve
   - Document lessons learned

---

**Last Updated:** 2025-11-18
**Template Version:** 1.0
