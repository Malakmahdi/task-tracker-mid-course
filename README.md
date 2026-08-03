# FocusBoard Task Tracker

A small FastAPI task tracker with a responsive Kanban frontend. The mid-course
extension adds:

- optional due dates, overdue indicators, and an overdue-only filter;
- validated tags, tag chips, and case-insensitive tag filtering.

## Run the backend and frontend

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. API documentation is available at
<http://127.0.0.1:8000/docs>.

Data is intentionally stored in memory for this course-sized example. Restarting
the server clears tasks.

## Run tests

```bash
pytest -q
```

The submission documentation is in [`docs/midcourse`](docs/midcourse).

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker still runs inside the intended course scope.
- CI runs the pytest suite on pushes and pull requests.
- The Docker image runs as a non-root user and `/health` returns HTTP 200.
- AI review, security, and ownership evidence is recorded in `docs/`.

### How to run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. The FastAPI process serves the Kanban frontend
from `frontend/`. Check the API at <http://127.0.0.1:8000/docs> and health at
<http://127.0.0.1:8000/health>.

### How to run tests

```bash
python -m pytest -q
```

### How to run with Docker

```bash
docker build -t task-tracker:final .
docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final
curl http://127.0.0.1:8000/health
```

The expected health response is `{"status":"ok"}` with HTTP 200. Stop the
foreground container with `Ctrl+C`.

### Evidence files

- [`docs/release-evidence.md`](docs/release-evidence.md)
- [`docs/final-ai-review.md`](docs/final-ai-review.md)
- [`docs/ai-playbook.md`](docs/ai-playbook.md)

### AI assistance summary

AI helped draft and review CI, Docker, release documentation, and the security
mini-review. I verified the work with the full test suite, diff inspection,
Docker build/run checks, `/health`, and a manual secret scan. I rejected the
suggestion to copy the entire repository into the image because a narrow copy of
`app/`, `frontend/`, and `requirements.txt` reduces accidental data exposure.
