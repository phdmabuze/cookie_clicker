import math

from django.utils import timezone
from ninja import Router

from authorization.util import AuthBearer, validate_token
from users.models import TgUser
from users.schemas import UserInfoSchema

router = Router()

@router.get("/{user_tg_id}", auth=AuthBearer())
def get_user_info(request, user_tg_id: int) -> UserInfoSchema:
    validate_token(request.auth, user_tg_id)
    user = TgUser.objects.get(tg_id=user_tg_id)
    return UserInfoSchema(
        username=user.get_username(),
        balance=user.get_balance_with_income(),
        income_per_second=user.income_per_second,
        photo_url=user.photo_url,
    )