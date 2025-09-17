from ninja import Router
from ninja.errors import HttpError

from authorization.schemas import LoginDataSchema, WebAppInitDataSchema
from authorization.util import validate_init_data_hash, build_token
from django.conf import settings

from users.models import TgUser

router = Router()

@router.post("/web-app", response={201: str})
def auth_by_webapp_init_data(request, login_data: LoginDataSchema):
    try:
        webapp_init_data = WebAppInitDataSchema.from_str(login_data.init_data)
    except:
        raise HttpError(status_code=400, message="Unable to parse init data")
    if not settings.TESTING and not validate_init_data_hash(webapp_init_data, settings.BOT_TOKEN.encode()):
        raise HttpError(status_code=400, message="Init Data hash is invalid")
    try:
        user = TgUser.objects.get(tg_id=webapp_init_data.user.id)
    except TgUser.DoesNotExist:
        user = TgUser(
            tg_id=webapp_init_data.user.id,
            username=webapp_init_data.user.username,
            first_name=webapp_init_data.user.first_name,
            last_name=webapp_init_data.user.last_name,
            photo_url=webapp_init_data.user.photo_url,
        )
        user.save()
    return 201, build_token(user)

