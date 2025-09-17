import datetime
import time
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone
from ninja.testing import TestClient

from upgrades.api import router
from upgrades.models import Upgrade
from users.models import TgUser
from users.api import router as users_router


@override_settings(TESTING=True)
class UpgradesTest(TestCase):
    def test_get_user_info(self):
        test_user = TgUser.objects.create(tg_id=1, balance=200)
        client = TestClient(router, headers={"Authorization": f"Bearer test_token"})
        response = client.get(f"/{test_user.tg_id}/upgrades")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data, [])

        test_upgrade = Upgrade.objects.create(name="test_upgrade", price=100, income_increase=10)
        response = client.get(f"/{test_user.tg_id}/upgrades")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()[0]
        self.assertEqual(data["name"], test_upgrade.name)
        self.assertEqual(data["price"], test_upgrade.price)
        self.assertEqual(data["income_increase"], test_upgrade.income_increase)
        self.assertEqual(data["photo_url"], test_upgrade.photo_url)
        self.assertEqual(data["is_purchased"], False)
        self.assertEqual(data["id"], test_upgrade.id)

        response = client.post(f"/{test_user.tg_id}/upgrades/{test_upgrade.id}")
        self.assertEqual(response.status_code, 201, response.json())

        response = client.get(f"/{test_user.tg_id}/upgrades")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()[0]
        self.assertEqual(data["is_purchased"], True)

        users_client = TestClient(users_router, headers={"Authorization": f"Bearer test_token"})
        response = users_client.get(f"/{test_user.tg_id}")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data["income_per_second"], test_upgrade.income_increase + settings.DEFAULT_INCOME_PER_SECOND)
        self.assertEqual(data["balance"], test_user.balance - test_upgrade.price)

        response = client.post(f"/{test_user.tg_id}/upgrades/{test_upgrade.id}")
        self.assertEqual(response.status_code, 400, response.json())

        test_upgrade_2 = Upgrade.objects.create(name="test_upgrade_2", price=100, income_increase=10)
        response = client.get(f"/{test_user.tg_id}/upgrades")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data[0]["is_purchased"], True)
        self.assertEqual(data[1]["is_purchased"], False)

        response = client.post(f"/{test_user.tg_id}/upgrades/{test_upgrade_2.id}")
        self.assertEqual(response.status_code, 201, response.json())

        response = client.get(f"/{test_user.tg_id}/upgrades")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data[0]["is_purchased"], True)
        self.assertEqual(data[1]["is_purchased"], True)

        response = users_client.get(f"/{test_user.tg_id}")
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertEqual(data["income_per_second"], test_upgrade.income_increase + test_upgrade_2.income_increase + settings.DEFAULT_INCOME_PER_SECOND)
        self.assertEqual(data["balance"], test_user.balance - test_upgrade.price - test_upgrade_2.price)

    def test_income(self):
        test_user = TgUser.objects.create(tg_id=1)
        users_client = TestClient(users_router, headers={"Authorization": f"Bearer test_token"})
        upgrades_client = TestClient(router, headers={"Authorization": f"Bearer test_token"})
        test_upgrade = Upgrade.objects.create(name="test_upgrade", price=12, income_increase=10)
        start_time = timezone.now()
        with patch('utils.get_time', return_value=start_time + datetime.timedelta(seconds=10)):
            response = users_client.get(f"/{test_user.tg_id}")
            self.assertEqual(response.status_code, 200, response.json())
            data = response.json()
            self.assertEqual(data["balance"], 10)

            response = upgrades_client.post(f"/{test_user.tg_id}/upgrades/{test_upgrade.id}")
            self.assertEqual(response.status_code, 400, response.json())

        with patch('utils.get_time', return_value=start_time + datetime.timedelta(seconds=12)):
            response = upgrades_client.post(f"/{test_user.tg_id}/upgrades/{test_upgrade.id}")
            self.assertEqual(response.status_code, 201, response.json())
            response = users_client.get(f"/{test_user.tg_id}")
            self.assertEqual(response.status_code, 200, response.json())
            data = response.json()
            self.assertEqual(data["balance"], 0)
            self.assertEqual(data["income_per_second"], test_upgrade.income_increase + settings.DEFAULT_INCOME_PER_SECOND)

        with patch('utils.get_time', return_value=start_time + datetime.timedelta(seconds=12 + 9)):
            response = users_client.get(f"/{test_user.tg_id}")
            self.assertEqual(response.status_code, 200, response.json())
            data = response.json()
            self.assertEqual(data["balance"], (test_upgrade.income_increase + settings.DEFAULT_INCOME_PER_SECOND) * 9)


