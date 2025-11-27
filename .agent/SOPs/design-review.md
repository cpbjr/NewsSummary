# SOP: Comprehensive Design Review

**Purpose**: Perform thorough UI/UX design review using browser-mcp automation

**When to Use**:
- Before creating pull requests with UI changes
- After completing significant UI refactors
- When user explicitly requests design review
- For new features with substantial frontend work

**Prerequisites**: See below

---

## Prerequisites

Before starting design review:

- [ ] Dev server is running (usually `npm run dev` or similar)
- [ ] browser-mcp is installed and accessible (check with `/mcp` command)
- [ ] Design principles exist (`.agent/Design/design-principles.md`)
- [ ] Changes are committed or saved locally
- [ ] Know which pages/components to review

**If prerequisites not met**:
- Start dev server first
- Verify browser-mcp: `/mcp` command should list it
- If design-principles.md missing, create from template first

---

## Procedure

### 1. Context Gathering

**Read design resources**:
1. Read `.agent/Design/design-principles.md` (typography, colors, spacing, components)
2. Read `.agent/Design/style-guide.md` (brand, patterns, writing style)
3. Read `PRD.md` or `.agent/Tasks/current-sprint.md` (understand project goals)

**Understand changes**:
- What files were modified?
- What features/components are affected?
- What pages need to be reviewed?
- Any specific acceptance criteria from user?

**Document in notes**:
```
Files changed:
- src/components/RecipeCard.tsx
- src/pages/RecipeList.tsx

Features affected:
- Recipe card display
- Recipe grid layout

Pages to review:
- /recipes (list view)
- /recipes/123 (detail view)

Acceptance criteria:
- Cards should match design-principles.md
- Mobile responsive (375px, 768px, 1920px)
- No console errors
```

### 2. Visual Analysis with browser-mcp

#### Desktop Testing (1920x1080)

**Steps**:
1. Launch browser-mcp (use appropriate tool)
2. Navigate to `http://localhost:[PORT]` (check dev server port)
3. Set viewport to 1920x1080 (desktop)
4. Navigate through affected pages/components
5. Capture screenshots of ALL states:
   - **Default state**: Initial page load
   - **Hover states**: Buttons, cards, links (if applicable)
   - **Active/focus states**: Form inputs, interactive elements
   - **Error states**: Form validation, error messages
   - **Empty states**: No data/content scenarios
   - **Loading states**: Spinners, skeletons, progress indicators

**Screenshot naming**:
- `desktop-recipes-default.png`
- `desktop-recipe-card-hover.png`
- `desktop-form-error.png`

#### Tablet Testing (768x1024)

**Steps**:
1. Resize viewport to 768x1024 (tablet)
2. Re-test same pages/components
3. Capture screenshots of key views
4. Note layout shifts or issues:
   - Does grid change columns appropriately?
   - Does navigation adapt (hamburger menu)?
   - Are touch targets adequate (44x44px minimum)?
   - Is text readable (no tiny fonts)?

**Look for**:
- Appropriate column counts in grids
- Navigation changes (inline → hamburger)
- Font size adjustments
- Spacing adjustments

#### Mobile Testing (375x667)

**Steps**:
1. Resize viewport to 375x667 (mobile - iPhone SE)
2. Re-test with mobile considerations:
   - **Touch target sizes**: Buttons, links ≥ 44x44px
   - **Readability**: Text ≥ 16px (prevents iOS zoom)
   - **Navigation**: Hamburger menu works correctly
   - **Horizontal scrolling**: Should NOT occur
   - **Forms**: Stacked layout, easy to fill
   - **Images**: Responsive, not cut off

**Capture screenshots** of:
- Homepage mobile view
- Navigation menu open
- Form on mobile
- Any problematic areas

### 3. Technical Analysis

#### Console Errors

**Check browser console for**:
- **JavaScript errors**: Red error messages
- **React warnings**: Yellow warnings (key props, deprecated APIs)
- **Network errors**: 404s, 500s, failed requests
- **Performance warnings**: Slow components, memory leaks

**Document all errors**:
```
Console Errors:
1. TypeError: Cannot read property 'name' of undefined
   Location: RecipeCard.tsx:45
   Severity: HIGH (breaks functionality)

2. Warning: Each child in list should have unique key prop
   Location: RecipeList.tsx:30
   Severity: MEDIUM (React warning)
```

#### Accessibility

**Keyboard navigation test**:
1. Tab through ALL interactive elements
2. Verify focus indicators are visible (not hidden by outline: none)
3. Check tab order is logical (top-to-bottom, left-to-right)
4. Test Enter/Space on buttons
5. Test Arrow keys in custom widgets (if applicable)
6. Test Escape to close modals/menus

**Screen reader test** (if available):
- Use NVDA (Windows) or VoiceOver (Mac)
- Navigate page with screen reader only
- Verify all content is announced
- Check ARIA labels are appropriate
- Test form labels and error messages

**Color contrast check**:
- Use browser DevTools accessibility panel
- Check all text colors meet 4.5:1 ratio (normal text)
- Check all text colors meet 3:1 ratio (large text ≥18px)
- Verify UI components have 3:1 contrast

**Semantic HTML check**:
- Inspect HTML structure
- Verify proper use of semantic elements (nav, main, article, header, footer)
- Check headings are in proper order (h1 → h2 → h3, no skipping)
- Verify buttons are `<button>` not `<div onclick>`

#### Performance

**Visual checks**:
- Note any slow-loading images (should load quickly)
- Check for layout shifts (CLS - content jumping)
- Verify smooth animations (no janky/stuttering)
- Test scroll performance (should be smooth)

**If slow**:
- Note which parts are slow
- Suggest optimizations (lazy loading, code splitting, image optimization)

### 4. Comparison Against Standards

Use design-principles.md as checklist:

#### Visual Design

- [ ] **Typography scale followed?**
  - Check: h1, h2, h3, body text match defined sizes
  - Example: h1 should be 2.5rem (40px)

- [ ] **Color palette consistent?**
  - Check: Colors used are from defined palette
  - No random colors (#1E90FF when palette uses #3B82F6)

- [ ] **Spacing scale applied correctly?**
  - Check: Padding, margins use scale values (4px, 8px, 16px, 24px...)
  - No arbitrary spacing (padding: 15px should be padding: 16px)

- [ ] **Component guidelines followed?**
  - Buttons: Correct height, padding, border radius?
  - Cards: Correct padding, shadow, border radius?
  - Forms: Label above input, helper text below, correct heights?

- [ ] **Animations appropriate?**
  - Duration: 150-300ms (not longer than 500ms)
  - Easing: Appropriate timing function
  - Respects prefers-reduced-motion

#### Accessibility (WCAG 2.1 AA)

- [ ] **Contrast ratio adequate?**
  - Normal text: 4.5:1 minimum
  - Large text (≥18px): 3:1 minimum
  - UI components: 3:1 minimum

- [ ] **Keyboard navigation works?**
  - All interactive elements reachable with Tab
  - Tab order is logical
  - Enter/Space activates buttons

- [ ] **Focus indicators visible?**
  - Focus ring or outline clearly visible
  - Not hidden by outline: none without alternative

- [ ] **Semantic HTML used?**
  - Buttons are `<button>`, not `<div onclick>`
  - Navigation is `<nav>`
  - Headings are proper hierarchy

- [ ] **ARIA labels where needed?**
  - Icon-only buttons have aria-label
  - Form inputs have labels
  - Status messages use aria-live

#### Responsive Design

- [ ] **Works on mobile (375px)?**
  - No horizontal scrolling
  - Touch targets ≥ 44x44px
  - Text ≥ 16px (body)
  - Navigation adapted (hamburger)

- [ ] **Works on tablet (768px)?**
  - Appropriate column counts
  - Layout adapts logically
  - Touch targets adequate

- [ ] **Works on desktop (1920px)?**
  - Max-width container prevents over-stretching
  - Layout uses space effectively
  - No excessive whitespace

#### Code Quality

- [ ] **Follows component structure conventions?**
  - File organization correct
  - Naming conventions followed
  - Imports organized

- [ ] **Uses approved tech stack?**
  - No unauthorized libraries
  - Follows tech-stack.md guidelines

- [ ] **No duplicate code?**
  - Components reused appropriately
  - Utilities extracted where needed

- [ ] **Proper error handling?**
  - Try-catch for async operations
  - Error boundaries for React errors
  - User-friendly error messages

- [ ] **Loading states implemented?**
  - Spinners or skeletons for async operations
  - Disabled states during processing
  - Feedback within 100ms

### 5. Generate Review Report

Create comprehensive report using this format:

```markdown
# Design Review Report

**Date**: [Current date - YYYY-MM-DD]
**Reviewer**: Claude Code (browser-mcp automated)
**Scope**: [Files/pages reviewed]

---

## Overall Assessment

[1-2 sentence summary of overall quality]

**Grade**: [A/B/C/D based on compliance]
- A: Excellent (0-2 minor issues)
- B: Good (3-5 minor issues or 1 moderate issue)
- C: Needs improvement (6+ minor or 2+ moderate issues)
- D: Significant problems (any high-priority issues)

---

## Screenshots

### Desktop (1920x1080)

[Describe what was captured, attach screenshots if possible]
- Homepage default state
- Recipe card hover state
- Form error state

### Tablet (768x1024)

[Describe tablet views]
- Homepage (grid changed to 2 columns)
- Navigation (hamburger menu)

### Mobile (375x667)

[Describe mobile views]
- Homepage (single column)
- Navigation menu (drawer)
- Form (stacked inputs)

---

## Findings

### ✅ Strengths

[Specific positive observations - what's working well]
- Typography scale correctly applied across all headings
- Color palette consistently used
- Smooth animations with appropriate durations
- Excellent keyboard navigation support

### 🔴 High Priority Issues

**Visual Design:**
- [Critical design problems that significantly impact user experience]
- Example: "Primary button uses #1E90FF instead of defined primary color #3B82F6"

**Accessibility:**
- [WCAG violations that exclude users with disabilities]
- Example: "Form error text has 2.8:1 contrast, needs 4.5:1 minimum (WCAG AA violation)"

**Performance:**
- [Critical performance issues affecting usability]
- Example: "Recipe images load slowly (3-5 seconds), need optimization"

**Functionality:**
- [Broken features or critical bugs]
- Example: "Save button doesn't work when recipe name is empty (no validation)"

### 🟡 Medium Priority Issues

[Important but not critical - should be addressed before production]
- Button hover state darkens only 5% instead of 10% (design-principles.md line 159)
- Card padding is 20px instead of 24px (design-principles.md line 162)
- Missing loading state on import button

### 🟢 Low Priority / Polish

[Nice-to-have refinements, future enhancements]
- Consider adding transition to navigation on scroll
- Empty state could use illustration instead of just text
- Success toast could include confetti animation

---

## Recommendations

### 1. [Specific, actionable recommendation]

**Location**: src/components/RecipeCard.tsx:45
**Fix**: Change button color from `#1E90FF` to `primary` color variable
**Reason**: Consistency with design system (design-principles.md line 114)
**Priority**: HIGH

### 2. [Another recommendation]

**Location**: src/pages/RecipeList.tsx:72
**Fix**: Add `alt` attribute to recipe images
**Reason**: Accessibility requirement (screen readers need image descriptions)
**Priority**: HIGH

### 3. [Another recommendation]

**Location**: src/components/ImportModal.tsx:30
**Fix**: Add loading state to Import button with spinner
**Reason**: Users need feedback during async operation (style-guide.md loading states)
**Priority**: MEDIUM

---

## Console Errors

[List any console errors/warnings found, or "None"]

**Errors:**
1. TypeError: Cannot read property 'name' of undefined (RecipeCard.tsx:45)
2. Network error: Failed to fetch /api/recipes (404)

**Warnings:**
1. React Warning: Each child in list should have unique key prop (RecipeList.tsx:30)

---

## Accessibility Audit

- **Keyboard Navigation**: ❌ FAIL - Recipe cards not keyboard accessible (need tabindex or button wrapper)
- **Color Contrast**: ⚠️ PARTIAL - Most text passes, error text fails (2.8:1, needs 4.5:1)
- **Semantic HTML**: ✅ PASS - Proper use of nav, main, article, button elements
- **ARIA Labels**: ✅ PASS - All icon buttons have appropriate aria-label
- **Focus Indicators**: ✅ PASS - Clear focus rings on all interactive elements

---

## Next Steps

- [ ] Fix high-priority button color inconsistency
- [ ] Fix high-priority accessibility: keyboard navigation for cards
- [ ] Fix high-priority accessibility: error text contrast
- [ ] Add alt attributes to all images
- [ ] Add loading state to Import button
- [ ] (Optional) Add illustrations to empty states

**Estimated effort**: 2-3 hours to address high/medium priority issues

---

**End of Review**
```

### 6. Update Documentation

After completing review:

**If issues found**:
- Update `.agent/Tasks/current-sprint.md` with fix tasks
- Create follow-up tasks for medium/low priority items

**If new patterns discovered**:
- Document in `.agent/SOPs/` if repeatable procedure
- Update `.agent/Design/design-principles.md` if new patterns should be standard

**Update README**:
- Reference this review in `.agent/README.md` if significant

---

## Guidelines

### Be Specific

❌ **Vague**: "Improve the design"
✅ **Specific**: "Increase button padding from 8px to 12px to match design system (design-principles.md line 155)"

❌ **Vague**: "Fix accessibility"
✅ **Specific**: "Add aria-label='Close dialog' to X button in modal (missing screen reader text)"

### Prioritize by Impact

**High Priority** (must fix before merge):
- User-facing bugs (functionality broken)
- Accessibility violations (excludes users)
- Broken responsive layout (mobile unusable)
- Critical performance issues (page hangs)

**Medium Priority** (should fix before production):
- Design inconsistencies (wrong colors, spacing)
- Minor UX issues (confusing labels)
- Non-critical console warnings
- Missing loading states

**Low Priority** (nice-to-have):
- Polish and micro-interactions
- Optional animations
- Subjective improvements
- Future enhancements

### Balance Feedback

**Do**:
- Recognize good work alongside criticism
- Provide visual comparisons when helpful (before/after)
- Suggest concrete solutions, not just problems
- Explain why something matters (user impact, accessibility, performance)

**Don't**:
- Only list problems without acknowledging strengths
- Be vague or subjective ("looks bad")
- Criticize without providing solution
- Overwhelm with too many low-priority items

### Reference Standards

**Always cite sources**:
- design-principles.md line numbers
- style-guide.md sections
- WCAG 2.1 guidelines (link: https://www.w3.org/WAI/WCAG21/quickref/)
- tech-stack.md for technology decisions

**Example**:
"Button height should be 40px, not 36px (design-principles.md line 155, Component Guidelines → Buttons)"

---

## Common Issues Checklist

Use this as quick reference during review:

### Visual Issues

- [ ] Colors outside defined palette (random hex values)
- [ ] Inconsistent spacing (not using scale: 4px, 8px, 16px, 24px...)
- [ ] Typography not following hierarchy (wrong font sizes)
- [ ] Missing hover/focus states on interactive elements
- [ ] Animations too long (>500ms)
- [ ] Pure black (#000000) used instead of off-black

### Accessibility Issues

- [ ] Insufficient contrast (<4.5:1 for normal text)
- [ ] Missing keyboard navigation (can't tab to element)
- [ ] No focus indicators (outline: none without replacement)
- [ ] Non-semantic HTML (divs for buttons, etc.)
- [ ] Missing alt text on images
- [ ] Form inputs without associated labels
- [ ] Missing ARIA labels on icon-only buttons

### Responsive Issues

- [ ] Horizontal scrolling on mobile
- [ ] Touch targets too small (<44px)
- [ ] Text too small on mobile (<16px body text)
- [ ] Layout breaks at certain widths
- [ ] Images not responsive (fixed width cuts off)
- [ ] Navigation doesn't adapt (no hamburger menu)

### Code Issues

- [ ] Console errors present (JavaScript errors, React warnings)
- [ ] Missing loading states (no spinner during async operations)
- [ ] No error handling (try-catch, error boundaries)
- [ ] Duplicate code (should extract to utility/component)
- [ ] Not using approved tech stack (unauthorized dependencies)
- [ ] Poor file organization (doesn't follow conventions)

---

## Notes

**Customization needed**: Minimal
- Update viewport sizes if project has custom breakpoints
- Update dev server URL/port if different from localhost:3000/5173
- Reference project-specific design docs paths

**Works as-is for**:
- Any React-based project
- Any project with browser-mcp
- Any project with design-principles.md and style-guide.md

**Adapt for**:
- Vue/Svelte projects (adjust component examples)
- Non-Tailwind projects (adjust CSS class references)
- Different dev server setups (adjust URLs)

---

**Last Updated**: [YYYY-MM-DD]
**Template Version**: 1.0
**Related Documents**: design-principles.md, style-guide.md, tech-stack.md
