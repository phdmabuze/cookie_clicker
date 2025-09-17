import datetime
import time
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone
from ninja.testing import TestClient, TestAsyncClient

from tasks.api import router
from tasks.models import Task, TaskCompletion
from users.models import TgUser
from users.api import router as users_router


@override_settings(TESTING=True)
class TasksTest(TestCase):
    async def test_get_tasks(self):
        test_user = await TgUser.objects.acreate(tg_id=1)
        client = TestAsyncClient(router, headers={"Authorization": "Bearer test_token"})
        response = await client.get(f"/{test_user.tg_id}/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        test_task = await Task.objects.acreate(name="test_task", description="test_description", channel_id=1, reward=1)
        response = await client.get(f"/{test_user.tg_id}/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["status"], "ready", response.json()[0])

        response = await client.post(f"/{test_user.tg_id}/tasks/{test_task.id}")
        self.assertEqual(response.status_code, 201, response.json())

        with patch("utils.check_tg_subscription", return_value=False):
            response = await client.get(f"/{test_user.tg_id}/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()[0]["status"], "pending", response.json()[0])

        with patch("utils.check_tg_subscription", return_value=False):
            response = await client.get(f"/{test_user.tg_id}/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()[0]["status"], "pending", response.json()[0])

        with patch("utils.get_time", return_value=timezone.now() + datetime.timedelta(seconds=settings.TASK_COMPLETION_PENDING_TIME + 10)):
            response = await client.get(f"/{test_user.tg_id}/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()[0]["status"], "ready", response.json()[0])
            response = await client.post(f"/{test_user.tg_id}/tasks/{test_task.id}")
            self.assertEqual(response.status_code, 201, response.json())

            with patch("utils.check_tg_subscription", return_value=False):
                response = await client.get(f"/{test_user.tg_id}/tasks")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()[0]["status"], "pending", response.json()[0])


            balance = (await TgUser.objects.aget(tg_id=test_user.tg_id)).balance
            with patch("utils.check_tg_subscription", return_value=True):
                response = await client.get(f"/{test_user.tg_id}/tasks")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()[0]["status"], "completed", response.json()[0])

                self.assertEqual((await TgUser.objects.aget(tg_id=test_user.tg_id)).balance - balance, test_task.reward)


