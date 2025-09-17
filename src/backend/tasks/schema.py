import enum
from typing import Literal
from ninja import Schema

class TaskStatus(str, enum.Enum):
    READY = "ready"
    PENDING = "pending"
    COMPLETED = "completed"

class TaskSchema(Schema):
    id: int
    name: str
    description: str
    channel_id: str | int
    status: TaskStatus
