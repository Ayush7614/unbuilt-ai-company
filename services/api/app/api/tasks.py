from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskStatusUpdate
from app.services.tasks import (
    InvalidTaskTransitionError,
    TaskNotFoundError,
    create_task,
    get_task,
    list_tasks,
    update_task_status,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(payload: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, payload)


@router.get("", response_model=list[TaskRead])
def list_tasks_endpoint(limit: int = Query(default=50, ge=1, le=100), db: Session = Depends(get_db)):
    return list_tasks(db, limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    try:
        return get_task(db, task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found") from None


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status_endpoint(task_id: str, payload: TaskStatusUpdate, db: Session = Depends(get_db)):
    try:
        return update_task_status(db, task_id, payload)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found") from None
    except InvalidTaskTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
