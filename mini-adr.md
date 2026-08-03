# Mini-ADR: due dates and tags

**Status:** Accepted  
**Date:** 2026-07-30

## Context

The replacement Task Tracker needed two small features that cross the API,
tests, and Kanban UI. The design had to remain understandable and finishable.

## Decision

`due_date` is an optional Pydantic `date`. Overdue status is computed from the
current date in both the API filter and the UI indicator using the same rule:
the due date is before today and status is not `done`.

`tags` is a list of strings on each task. Input is trimmed, limited to five tags
of at most 20 characters, and deduplicated case-insensitively. Filtering uses
exact case-insensitive matching. The browser derives its tag dropdown from
loaded tasks.

## Alternatives considered

- A database migration and normalized tag/tag-join tables were rejected as too
  complex for the in-memory Modules 1–3 architecture.
- A persisted `is_overdue` field was rejected because it becomes stale when the
  date changes.
- Substring tag search was rejected because exact matching is predictable.
- A new frontend framework was rejected; plain HTML/CSS/JavaScript preserves the
  small project structure and avoids build tooling.

## Consequences

The implementation is compact and testable. Dates follow server-local calendar
time, and data does not survive a restart; both limits are explicit in the README.
