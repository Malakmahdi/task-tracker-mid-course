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
- Latest run link or note: workflow prepared for the `final-project` push. The
  hosted run will execute both pytest and the Docker build/run/health contract;
  record its URL after the branch is uploaded.
- Test command used by CI: `python -m pytest -q`
- Shortcut check: no `continue-on-error`, no `|| true`, pytest is not skipped,
  Python is `3.12.11`, and dependencies are installed from `requirements.txt`.

## Docker evidence

- Build command: `docker build -t task-tracker:final .`
- Run command: `docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final`
- `/health` check: this workstation has no Docker-compatible runtime installed,
  so a local container result is not claimed. The CI `docker` job builds the
  image, starts it, and requires `curl --fail http://127.0.0.1:8000/health`.
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
| Docker runs as non-root and serves `/health` | CI `docker` job checks `id -u`, builds, runs, and curls health | Pending first hosted run; local Docker unavailable | Added executable hosted verification instead of inventing a local result |
