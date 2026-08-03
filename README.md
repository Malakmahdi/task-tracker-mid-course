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
