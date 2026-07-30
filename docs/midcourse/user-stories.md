# User stories

## Feature 1: Due dates and overdue filtering

1. As a user, I want to add an optional due date so I can plan time-sensitive work.
   - Acceptance: create accepts an ISO `YYYY-MM-DD` date or no date.
   - Acceptance: invalid date strings return HTTP 422.
2. As a user, I want to edit or clear a due date when plans change.
   - Acceptance: PATCH can replace a date or set it to `null`.
   - Acceptance: unrelated updates preserve the existing date.
3. As a user, I want late work highlighted so I can act quickly.
   - Acceptance: a card is overdue only when its date is before today and it is not done.
   - Acceptance: overdue cards have a visible red label.
4. As a user, I want an overdue-only view so I can focus.
   - Acceptance: the filter keeps all Kanban columns visible.
   - Acceptance: empty columns retain a clear empty state.

**Corrected AI assumption:** an early assumption treated every past-due task as
overdue. Completed tasks are intentionally excluded because they no longer need
action.

## Feature 2: Tags and tag filtering

1. As a user, I want to add tags so I can group related tasks.
   - Acceptance: the API stores up to five trimmed tags.
   - Acceptance: blank tags and tags longer than 20 characters return HTTP 422.
2. As a user, I want duplicate tag input normalized.
   - Acceptance: duplicates are removed case-insensitively while the first spelling is retained.
3. As a user, I want tag chips on cards so categories are visible at a glance.
   - Acceptance: each stored tag renders as a chip.
4. As a user, I want to filter by tag without losing the board layout.
   - Acceptance: matching is case-insensitive.
   - Acceptance: no matches return an empty result without an error.
5. As a user, I want unrelated edits to preserve tags.
   - Acceptance: a priority-only PATCH leaves tags unchanged.

**Corrected AI assumption:** a normalized tag table was initially considered.
For this in-memory course project, a validated list is smaller, easier to explain,
and sufficient for exact-match filtering.
