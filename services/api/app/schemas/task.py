from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    task_type: str = Field(min_length=1, max_length=100, pattern=r"^[a-z][a-z0-9_-]*$")
    input: dict[str, Any]


class TaskStatusUpdate(BaseModel):
    status: str
    result: dict[str, Any] | None = None
    error: str | None = Field(default=None, max_length=4000)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    task_type: str
    status: str
    input: dict[str, Any] = Field(validation_alias="input_data")
    result: dict[str, Any] | None = Field(validation_alias="result_data")
    error: str | None
    created_at: datetime
    updated_at: datetime
