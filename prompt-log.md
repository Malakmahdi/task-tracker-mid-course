# Prompt log

This log summarizes the real AI-assisted workflow used to reconstruct and extend
the project. Large transcripts are intentionally omitted.

## Feature 1: Due dates and overdue filtering

### Prompt 1 — weak, then rewritten

**Weak:** “Add due dates.”

**Rewritten:** “Add an optional ISO date to create/update task schemas. Define
overdue as a date before today on a non-done task. Add `GET /tasks?overdue=true`,
an HTML date input, a card badge, and tests for valid, invalid, update/clear, and
filter behavior. Do not add a database.”

**AI response:** proposed a Pydantic `date`, a derived filter, and UI comparison.
**Decision:** accepted the date type and derived state; edited the contract to
explicitly exclude completed tasks and allow clearing with `null`.

### Prompt 2 — backend constraint

**Prompt:** “Implement due-date support without changing existing CRUD behavior.
Keep PATCH partial and ensure omitted fields remain unchanged.”

**AI response:** used `model_dump(exclude_unset=True)` and model copying.
**Decision:** accepted after checking that explicit `null` remains distinguishable
from an omitted field.

### Prompt 3 — verification and break test

**Prompt:** “Write focused pytest cases for invalid formats, overdue detection,
done-task exclusion, and clearing a due date. Identify one mutation that should
make an important test fail.”

**AI response:** supplied date-relative tests and suggested removing the
`status != done` condition.
**Decision:** accepted the relative-date approach and used the suggested mutation
for the Break Test.

## Feature 2: Tags and tag filtering

### Prompt 1 — scope

**Prompt:** “Add tags as a validated list on each in-memory task. Trim values,
reject blanks, cap at five and 20 characters, deduplicate case-insensitively,
and avoid normalized database models.”

**AI response:** proposed a shared normalization function and validators.
**Decision:** accepted; retained the first spelling when duplicates differ only
by case.

### Prompt 2 — frontend

**Prompt:** “Add comma-separated tag input, card chips, and an exact tag filter.
Keep all Kanban columns visible and preserve empty states.”

**AI response:** proposed deriving filter options from current tasks.
**Decision:** accepted and added HTML escaping before rendering user content.

### Prompt 3 — verification and break test

**Prompt:** “Test blank rejection, normalization, preservation after an unrelated
PATCH, and case-insensitive filtering. Suggest a small mutation to prove one test
is meaningful.”

**AI response:** proposed changing tag comparison from `casefold()` to direct
equality.
**Decision:** accepted as the second Break Test mutation.

## Review notes

AI output was inspected for PATCH semantics, date-boundary behavior, validation
consistency, and unsafe HTML rendering. The final implementation was edited to
escape all task content and to keep completed late tasks out of the overdue view.
