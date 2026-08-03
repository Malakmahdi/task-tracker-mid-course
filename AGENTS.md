# Repository guardrails

## Read first

Before changing code, read `README.md`, the relevant tests, and the evidence
documents in `docs/`. Treat `docs/release-evidence.md` as the release contract.
Inspect the current diff before proposing a rewrite.

## Stack and commands

- Backend: Python 3.12, FastAPI, Pydantic, Uvicorn.
- Frontend: plain HTML, CSS, and JavaScript in `frontend/`, served by FastAPI.
- Tests: `python -m pytest -q`.
- Local app: `uvicorn app.main:app --reload`.
- Docker: `docker build -t task-tracker:final .` then
  `docker run --rm -p 8000:8000 task-tracker:final`.

## Project rules

- Do not add product features in final-project work.
- Preserve the in-memory architecture and existing API behavior.
- Do not add authentication, comments, notifications, or a production database.
- Never add secrets, tokens, `.env` files, credentials, production logs, or real
  personal/customer data.
- Keep dependencies pinned and avoid dangerous CI shortcuts such as
  `continue-on-error`, `|| true`, or skipped tests.
- Run the full test suite after every code or configuration change.

## Protected paths

Changes to `app/` or `frontend/` require a small bug fix, security fix, or a
documented release correction. Explain every such edit in
`docs/final-ai-review.md`. If an unexpected edit appears in either path, stop,
inspect it, and do not silently include it.

## AI usage

AI output is a draft. Verify commands, inspect diffs, grade review findings, and
reject suggestions that expand scope or cannot be explained. Read files before
editing them and prefer the smallest maintainable change.
