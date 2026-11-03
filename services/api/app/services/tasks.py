from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskStatusUpdate


class TaskNotFoundError(Exception):
    pass


class InvalidTaskTransitionError(Exception):
    pass


_ALLOWED_TRANSITIONS = {
    TaskStatus.PENDING.value: {TaskStatus.RUNNING.value, TaskStatus.CANCELLED.value},
    TaskStatus.RUNNING.value: {
        TaskStatus.COMPLETED.value,
        TaskStatus.FAILED.value,
        TaskStatus.CANCELLED.value,
    },
    TaskStatus.COMPLETED.value: set(),
    TaskStatus.FAILED.value: set(),
    TaskStatus.CANCELLED.value: set(),
}


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(task_type=payload.task_type, input_data=payload.input)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: str) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    return task


def list_tasks(db: Session, limit: int = 50) -> list[Task]:
    statement = select(Task).order_by(Task.created_at.desc()).limit(limit)
    return list(db.scalars(statement).all())


def update_task_status(db: Session, task_id: str, payload: TaskStatusUpdate) -> Task:
    task = get_task(db, task_id)
    requested = payload.status
    valid_statuses = {status.value for status in TaskStatus}
    if requested not in valid_statuses:
        raise InvalidTaskTransitionError(f"Unknown task status: {requested}")

    allowed = _ALLOWED_TRANSITIONS[task.status]
    if requested not in allowed:
        raise InvalidTaskTransitionError(f"Transition {task.status} -> {requested} is not allowed")

    if requested == TaskStatus.COMPLETED.value and payload.error:
        raise InvalidTaskTransitionError("A completed task cannot include an error")
    if requested == TaskStatus.FAILED.value and not payload.error:
        raise InvalidTaskTransitionError("A failed task must include an error summary")

    task.status = requested
    task.result_data = payload.result
    task.error = payload.error
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task
