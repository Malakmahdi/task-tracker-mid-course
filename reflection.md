# Reflection

I used Codex for four distinct roles: interpreting the course brief, narrowing
the feature scope, generating an initial implementation, and designing tests
that could challenge that implementation. I retained responsibility by turning
broad requests into explicit behavior contracts before accepting code. The two
features stayed intentionally small: due dates with an overdue view, and tags
with exact filtering. Both cross the model, API, tests, and visible Kanban UI.

AI helped most when it identified that Pydantic’s `date` type already provides
strict, useful validation and serialization. That avoided custom parsing code
and made the valid/invalid tests direct. It also suggested using
`exclude_unset=True` for PATCH updates. I checked this carefully because clearing
a due date with explicit `null` must behave differently from omitting the field.

AI slowed me down when it initially leaned toward a normalized tag model. That
would be reasonable in a persistent relational application, but it was larger
than this in-memory assignment needed. It would have introduced migrations,
join behavior, and deletion rules without improving the assessed workflow. I
rejected it and used a validated string list instead.

My review changed the overdue definition. A first-pass interpretation marked
any task with a past date as overdue, including completed tasks. I corrected the
rule to exclude `done` tasks and added a test specifically protecting that
decision. I also added output escaping to the frontend rendering path; task
titles, descriptions, assignees, and tags are user-provided and should not be
inserted as raw HTML.

The Break Tests were useful because they demonstrated that the tests were not
only producing green output. Temporarily removing the completed-task exclusion
made the overdue filter test fail. Temporarily making tag comparison
case-sensitive made the tag filter test fail. Restoring each condition returned
the suite to green. The process reinforced that AI-generated code is a draft:
the developer still owns the contract, reviews edge cases, tests behavior, and
decides which complexity is justified.
