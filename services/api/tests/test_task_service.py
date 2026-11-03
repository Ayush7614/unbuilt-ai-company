import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.schemas.task import TaskCreate, TaskStatusUpdate
from app.services.tasks import InvalidTaskTransitionError, create_task, update_task_status


def test_failed_task_requires_error_summary():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        task = create_task(db, TaskCreate(task_type="research", input={}))
        update_task_status(db, task.id, TaskStatusUpdate(status="running"))
        with pytest.raises(InvalidTaskTransitionError, match="must include an error"):
            update_task_status(db, task.id, TaskStatusUpdate(status="failed"))
    Base.metadata.drop_all(engine)
    engine.dispose()
