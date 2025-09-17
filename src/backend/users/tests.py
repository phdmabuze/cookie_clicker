import time

import jwt
from django.conf import settings
from django.test import TestCase, override_settings
from ninja.testing import TestClient

from authorization.util import build_token
from users.api import router
from users.models import TgUser


@override_settings(TESTING=True)
class UserInfoTest(TestCase):
    def test_get_user_info(self):
        test_user = TgUser.objects.create(tg_id=1)
        client = TestClient(router, headers={"Authorization": f"Bearer test_token"})
        response = client.get(f"/{test_user.tg_id}")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data["username"], "Player#1")
        self.assertEqual(data["balance"], 0)
        self.assertEqual(data["income_per_second"], 1)
        self.assertEqual(data["photo_url"], None)

    def test_get_user_info_with_username(self):
        test_user = TgUser.objects.create(tg_id=2, username="test_user")
        client = TestClient(router, headers={"Authorization": f"Bearer test_token"})
        response = client.get(f"/{test_user.tg_id}")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data["username"], "test_user")