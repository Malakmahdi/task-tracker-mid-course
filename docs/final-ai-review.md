# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/` or `frontend/` edits rule included: yes.

## Protected-path correction

The final brief requires `frontend/`, while the mid-course repository used
`static/`. I renamed that directory and changed only the resolved directory name
in `app/main.py`; no HTML, CSS, JavaScript, API, or product behavior changed.
The full tests and browser baseline were rerun after the correction.

## AI code review mini-log

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| Use a specific Python version in CI instead of an unspecified latest version. | Useful | Reproducibility is a release requirement. | Set `actions/setup-python` to `3.12.11`; requirements are pinned. |
| Add `--reload` to the Docker command for convenience. | Wrong | Reload is a development behavior and adds unnecessary runtime monitoring. | Rejected; Docker uses a clear exec-form Uvicorn command without reload. |
| Copy the whole repository into the Docker image. | Noise | It is easy but expands the build context and risks including docs or local artifacts. | Rejected; copy only requirements, `app/`, and `frontend/`; use `.dockerignore`. |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| Container could run as root. | `Dockerfile` | Valid | A compromised process should not receive root privileges by default. | Added system user/group and `USER app`; verify with `id`. |
| User task text rendered through `innerHTML` could create XSS. | `frontend/app.js`, `escapeHtml()` and `taskCard()` | Valid | The sink is sensitive, but title, description, assignee, and tags are escaped; priority/status are API enums. | Retain escaping and review any future rendered field before adding it. |
| API has no authentication. | `app/main.py` task routes | Noise | Authentication is explicitly outside the course scope and this is a local in-memory example, not a production service. | Document non-production scope; do not add an unreviewed auth feature. |
| In-memory tasks have no persistence or size limit. | `app/main.py`, `tasks` dictionary | Valid | An exposed long-running service could exhaust memory and loses data on restart. | Accept for course scope, keep local-only warning, revisit before production use. |

## Manual security check

I manually searched tracked files for token/key/password patterns, `.env` files,
credentials, logs, and personal/customer records. I also inspected the Docker
copy instructions rather than assuming `.dockerignore` alone prevents exposure.
No real secrets or personal/customer data were found; the example assignee in a
test is fictional course data. This matters because a public repository and
Docker build context can expose files that application tests never exercise.

## One AI output I rejected or corrected

AI proposed `COPY . .` as the simplest Dockerfile. I rejected it because the
release requirement emphasizes no baked secrets, and broad copying makes that
claim harder to verify. I instead copied only `requirements.txt`, `app/`, and
`frontend/`, backed by a defensive `.dockerignore`.

## Three AI usage rules

1. Never paste: secrets, tokens, `.env` values, private logs, or real personal/customer data.
2. Always verify: read the diff, run the relevant command, and check the behavior named in the claim.
3. Record AI contributions by: logging the suggestion, my grade, the evidence, and the final decision.

## Ownership statement

I am comfortable submitting this repository because I reviewed every final diff
and can explain the CI, Docker, test, and documentation choices. I ran the app,
checked `/health`, exercised the visible Kanban/create flow, and used tests and
manual inspection instead of accepting AI output blindly. I rejected suggestions
that expanded scope or weakened the container boundary. The final branch stays
within the course architecture and clearly records its remaining limitations.
