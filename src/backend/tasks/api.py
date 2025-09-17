import datetime

from django.conf import settings
from django.db.models import Q, F
from ninja import Router
from ninja.errors import HttpError

import utils
from authorization.util import AuthBearer, validate_token
from tasks.models import Task, TaskCompletion
from tasks.schemas import TaskSchema, TaskStatus
from users.models import TgUser

router = Router()


@router.get("/{user_tg_id}", auth=AuthBearer(), response={200: list[TaskSchema]})
async def get_tasks(request, user_tg_id: int) -> list[TaskSchema]:
    validate_token(request.auth, user_tg_id)
    tasks: dict[int, TaskSchema] = {
        t.id: TaskSchema(
            id=t.id,
            name=t.name,
            description=t.description,
            channel_id=t.channel_id,
            status=TaskStatus.READY,
            reward=t.reward,
            photo=t.photo,
            invite_link=t.invite_link,
        )  async for t in Task.objects.all()
    }
    async for t in TaskCompletion.objects.select_related("task").filter(user_id=user_tg_id).filter(
            Q(completed_at__isnull=False) | Q(
                created_at__gt=utils.get_time() - datetime.timedelta(seconds=settings.TASK_COMPLETION_PENDING_TIME))
    ):
        if t.completed_at is not None:
            tasks[t.task.id].status = TaskStatus.COMPLETED
            continue
        if await utils.check_tg_subscription(user_tg_id, t.task.channel_id):
            tasks[t.task.id].status = TaskStatus.COMPLETED
            await TaskCompletion.objects.filter(pk=t.pk).aupdate(completed_at=utils.get_time())
            user = await TgUser.objects.aget(tg_id=user_tg_id)
            await TgUser.objects.filter(tg_id=user_tg_id).aupdate(
                balance=user.get_balance_with_income() + t.task.reward,
                balance_last_updated_at=utils.get_time(),
            )
            continue
        tasks[t.task.id].status = TaskStatus.PENDING
    return list(tasks.values())


@router.post("/{user_tg_id}/start-completion/{task_id}", auth=AuthBearer(), response={201: str})
async def start_task(request, user_tg_id: int, task_id: int) -> str:
    validate_token(request.auth, user_tg_id)
    if (
            await TaskCompletion.objects.filter(user_id=user_tg_id, task_id=task_id)
                    .filter(Q(completed_at__isnull=False) | Q(
                created_at__gt=utils.get_time() - datetime.timedelta(seconds=settings.TASK_COMPLETION_PENDING_TIME)))
                    .aexists()
    ):
        raise HttpError(status_code=400, message="Task already completed or in progress")
    await TaskCompletion.objects.acreate(user_id=user_tg_id, task_id=task_id, created_at=utils.get_time())
    return "Task started"
