# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-03
- Local app run command: `.venv\\Scripts\\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `/health` result: HTTP 200 with `{"status":"ok"}`.
- Frontend check: opened `http://127.0.0.1:8000`; all three Kanban columns were
  visible and the Create a task modal opened from **+ New task**.
- Test command: `.venv\\Scripts\\python.exe -m pytest -q`
- Test result: `10 passed in 0.28s`.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run: [CI #1 - Success](https://github.com/Malakmahdi/task-tracker-mid-course/actions/runs/31255644584),
  triggered by the `final-project` push on 2026-08-08. Both the `test` and
  `docker` jobs passed in 32 seconds.
- Test command used by CI: `python -m pytest -q`
- Shortcut check: no `continue-on-error`, no `|| true`, pytest is not skipped,
  Python is `3.12.11`, and dependencies are installed from `requirements.txt`.

## Docker evidence

- Build command: `docker build -t task-tracker:final .`
- Run command: `docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final`
- `/health` check: the successful CI `docker` job built the image, started the
  container, and passed `curl --fail http://127.0.0.1:8000/health`. This
  workstation has no Docker-compatible runtime installed, so no local container
  result is claimed.
- Non-root check: image declares `USER app`; runtime identity will be checked with
  `docker run --rm task-tracker:final id`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, Git data,
  logs, tests, and docs; the Dockerfile copies only requirements, `app/`, and
  `frontend/`.
- Runtime command: exec-form `CMD` starts Uvicorn without development reload.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `python -m pytest -q` runs the suite | Clean virtual environment and pytest output | Pass: 10 tests | None |
| `GET /health` returns HTTP 200 and `{"status":"ok"}` | Running Uvicorn plus `Invoke-WebRequest` | Pass | None |
| FastAPI serves the Kanban frontend | Browser check at `/`, three columns and modal | Pass | Renamed `static/` to required `frontend/` and updated the documented server path |
| Docker runs as non-root and serves `/health` | Successful CI #1 `docker` job checks `id -u`, builds, runs, and curls health | Pass | Kept executable hosted verification and did not invent a local result |
