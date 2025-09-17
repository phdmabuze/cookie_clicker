import enum

from ninja import Schema


class TaskStatus(str, enum.Enum):
    READY = "ready"
    PENDING = "pending"
    COMPLETED = "completed"


class TaskSchema(Schema):
    id: int
    name: str
    description: str
    channel_id: str
    photo: str | None
    reward: int
    status: TaskStatus
    invite_link: str
