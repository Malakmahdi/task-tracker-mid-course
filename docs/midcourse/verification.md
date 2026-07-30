# Verification

## Baseline check

No prior Modules 1–3 repository was present locally or downloadable from the
course page. The agreed baseline was therefore a transparent reconstruction,
not a claim that earlier code existed. Before feature work, the replacement
contract was defined as in-memory CRUD with title, description, status,
priority, and assignee. Three regression tests cover create/list, status update,
and missing-delete behavior.

## Backend results

Final command:

```text
python -m pytest -q
..........                                                               [100%]
10 passed in 0.13s
```

Additional static checks:

- Python byte-compilation completed successfully.
- `node --check static/app.js` completed successfully.

Feature coverage includes valid and invalid dates, overdue calculation,
completed-task exclusion, clearing a date, tag normalization, blank-tag
rejection, preservation after unrelated PATCH, and case-insensitive filtering.

## Manual browser checks

Run at `http://127.0.0.1:8000` on 2026-07-30:

1. Opened the empty Kanban board; all three columns displayed empty states.
2. Created “Submit mid-course project” with high priority, due date 2026-07-29,
   assignee Malak, and tags `Course` and `Frontend`.
3. Confirmed the To do card displayed `Overdue · Jul 29, 2026`, both tag chips,
   assignee, priority, title, and description.
4. Enabled **Overdue only**; the result remained `1 task shown`.
5. Selected the `frontend` tag while overdue filtering remained enabled; the
   combined result remained `1 task shown`.
6. Confirmed the two nonmatching columns stayed visible with empty states.

## Behavior contract before and after refactor

The focused refactor centralized tag normalization and kept PATCH behavior based
on explicitly supplied fields. Before and after the refactor:

- omitted PATCH fields remain unchanged;
- explicit `due_date: null` clears the date;
- completed tasks are not overdue;
- tag matching is case-insensitive;
- all 10 tests pass.

## Break Test evidence

### Break Test 1: completed overdue tasks

Mutation: temporarily removed `task.status != TaskStatus.DONE` from the overdue
filter.

Observed result:

```text
FAILED test_overdue_filter_excludes_done_and_future_tasks
E assert [1, 3] == [1]
1 failed
```

The condition was restored and the test returned to passing.

### Break Test 2: case-insensitive tag matching

Mutation: temporarily changed the tag comparison from `casefold()` equality to
direct string equality.

Observed result:

```text
FAILED test_filter_by_tag_is_case_insensitive
E assert [] == [1]
1 failed
```

The case-insensitive comparison was restored and the full suite returned to
10 passing tests.
