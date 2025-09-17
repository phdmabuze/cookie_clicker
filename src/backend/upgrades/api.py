from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils import timezone
from ninja import Router
from django.db.models import Exists, OuterRef
from ninja.errors import HttpError

import utils
from authorization.util import AuthBearer, validate_token
from upgrades.models import UserUpgrade, Upgrade
from upgrades.schemas import UpgradeSchema
from users.models import TgUser

router = Router()

@router.get("/{user_tg_id}/upgrades", auth=AuthBearer(), response={200: list[UpgradeSchema]})
def get_user_upgrades(request, user_tg_id: int):
    validate_token(request.auth, user_tg_id)

    return Upgrade.objects.annotate(
        is_purchased=Exists(
            UserUpgrade.objects.filter(
                user_id=user_tg_id,
                upgrade_id=OuterRef("pk")
            )
        )
    )


@router.post("/{user_tg_id}/upgrades/{upgrade_id}", auth=AuthBearer(), response={201: str})
def purchase_upgrade(request, user_tg_id: int, upgrade_id: int):
    validate_token(request.auth, user_tg_id)
    try:
        user = TgUser.objects.get(tg_id=user_tg_id)
        upgrade = Upgrade.objects.get(pk=upgrade_id)
        if user.get_balance_with_income() < upgrade.price:
            raise HttpError(status_code=400, message="Not enough balance")
        with transaction.atomic():
            UserUpgrade.objects.create(
                user_id=user_tg_id,
                upgrade_id=upgrade_id
            )
            TgUser.objects.filter(tg_id=user_tg_id).update(
                balance=user.get_balance_with_income() - upgrade.price,
                income_per_second=user.income_per_second + upgrade.income_increase,
                balance_last_updated_at=utils.get_time(),
            )
    except IntegrityError:
        raise HttpError(status_code=400, message="Upgrade already purchased")
    return 201, "OK"
