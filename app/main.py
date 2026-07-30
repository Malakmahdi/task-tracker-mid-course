from __future__ import annotations

from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def normalize_tags(tags: list[str]) -> list[str]:
    if len(tags) > 5:
        raise ValueError("A task can have at most 5 tags")

    normalized: list[str] = []
    seen: set[str] = set()
    for raw_tag in tags:
        tag = raw_tag.strip()
        if not tag:
            raise ValueError("Tags cannot be blank")
        if len(tag) > 20:
            raise ValueError("Each tag must be 20 characters or fewer")
        key = tag.casefold()
        if key not in seen:
            normalized.append(tag)
            seen.add(key)
    return normalized


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    assignee: str | None = Field(default=None, max_length=60)
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("assignee")
    @classmethod
    def normalize_assignee(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return normalize_tags(value)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus | None = None
    priority: Priority | None = None
    assignee: str | None = Field(default=None, max_length=60)
    due_date: date | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("assignee")
    @classmethod
    def normalize_assignee(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str] | None) -> list[str] | None:
        return None if value is None else normalize_tags(value)


class Task(TaskBase):
    id: int


app = FastAPI(title="Task Tracker", version="2.0.0")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

tasks: dict[int, Task] = {}
next_task_id = 1


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    task_status: TaskStatus | None = Query(default=None, alias="status"),
    priority: Priority | None = None,
    overdue: bool = False,
    tag: Annotated[str | None, Query(max_length=20)] = None,
) -> list[Task]:
    today = date.today()
    result = list(tasks.values())
    if task_status is not None:
        result = [task for task in result if task.status == task_status]
    if priority is not None:
        result = [task for task in result if task.priority == priority]
    if overdue:
        result = [
            task
            for task in result
            if task.due_date is not None
            and task.due_date < today
            and task.status != TaskStatus.DONE
        ]
    if tag is not None:
        wanted = tag.strip().casefold()
        if not wanted:
            raise HTTPException(status_code=422, detail="Tag filter cannot be blank")
        result = [
            task
            for task in result
            if any(existing.casefold() == wanted for existing in task.tags)
        ]
    return sorted(result, key=lambda task: task.id)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    global next_task_id
    task = Task(id=next_task_id, **payload.model_dump())
    tasks[task.id] = task
    next_task_id += 1
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    existing = get_task(task_id)
    updates = payload.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=updates)
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
