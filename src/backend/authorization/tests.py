import time

import jwt
from django.conf import settings
from django.test import TestCase, override_settings
from ninja.testing import TestClient

from authorization.api import router
from users.models import TgUser

TEST_INIT_DATA = "query_id=AAEsBFUUAAAAACwEVRT-Kctd&user=%7B%22id%22%3A341115948%2C%22first_name%22%3A%22%D0%9F%D0%B0%D0%B2%D0%B5%D0%BB%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22poderzhimoimakintosh%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FHPg8hcmmBTqg8J3LiKHhBCeNcCU0ujzQEAP3D0aNRTA.svg%22%7D&auth_date=1758023895&signature=bQKOf2ef2roocy4Kp_5iioyW4L2XmHOGvLnbZzMH_699Si71j2tB1-JyG4ICxmhwbihD4cOfWaYRQCn-1r2UAg&hash=6b1d294634537cbcaf88cccb6c1c7db2801aa6f882ad97a99b66d947b7505e8c"

@override_settings(TESTING=True)
class UserAuthorizationTest(TestCase):
    def test_get_user_info(self):
        client = TestClient(router)
        response = client.post("/web-app", json={"init_data": TEST_INIT_DATA})
        self.assertEqual(response.status_code, 201, response.json())

        user = TgUser.objects.get(tg_id=341115948)
        self.assertEqual(user.photo_url, "https://t.me/i/userpic/320/HPg8hcmmBTqg8J3LiKHhBCeNcCU0ujzQEAP3D0aNRTA.svg")
        self.assertEqual(user.username, "poderzhimoimakintosh")
        self.assertEqual(user.first_name, "Павел")
        self.assertEqual(user.last_name, "")
        self.assertEqual(user.tg_id, 341115948)

        response = client.post("/web-app", json={"init_data": TEST_INIT_DATA})
        self.assertEqual(response.status_code, 201, response.json())