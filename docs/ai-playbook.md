# My AI Playbook

## When I reach for AI first

I use AI first when a task has a clear boundary but several details to remember:
turning a rubric into a checklist, drafting focused tests, reviewing a small
diff, comparing CI/Docker options, or generating failure hypotheses from real
evidence. It helped most when I supplied the actual file, expected behavior, and
constraints rather than asking for a complete rewrite.

## When I do not reach for AI first

I slow down when I lack repository context, when a change touches secrets or
permissions, when the action is destructive, or when I am still learning the
core concept being assessed. I inspect the existing code and reproduce the
problem first. I do not let AI invent test results, security evidence, or a
GitHub status that I have not observed.

## My non-negotiables

- Never provide secrets, tokens, `.env` values, private logs, or real personal/customer data.
- Read before editing and keep work inside the requested scope.
- Inspect every diff and be able to explain every submitted line.
- Run the relevant tests and behavior checks after changes.
- Treat AI review findings as claims to grade, not facts to obey.

## My review rules

I compare the diff with the acceptance criteria, trace inputs to outputs, and
look for error handling, unsafe defaults, and scope growth. I run the exact
commands that documentation promises. I grade findings Useful/Noise/Wrong or
Valid/False Positive/Noise, record why, and reject suggestions that add
complexity without evidence.

## What I am still figuring out

I am still learning when a team should require human approval for agent actions,
how much prompt/evidence history belongs in a long-lived repo, and when a small
tool-specific guardrail should become an organization-wide policy.

## Decision Card

| Situation | First move | One rule |
|---|---|---|
| New feature | Define acceptance criteria and exclusions | No code until scope is testable. |
| Code review | Give AI the real diff and contract | Grade every comment with evidence. |
| Debugging | Reproduce and capture the failure | Change one hypothesis at a time. |
| Infrastructure | Verify commands in the real environment | Reject shortcuts that hide failure. |
| Never paste | Secrets, private data, production logs | Redact or use synthetic examples. |
| Final ownership | Read diff, run checks, explain choices | If I cannot explain it, I do not submit it. |
