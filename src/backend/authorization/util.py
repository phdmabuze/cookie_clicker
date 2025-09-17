import hashlib
import hmac
from operator import itemgetter

import jwt
from django.conf import settings
from ninja.errors import HttpError
from ninja.security import HttpBearer

from authorization.schemas import WebAppInitDataSchema
from users.models import TgUser


def validate_init_data_hash(init_data: WebAppInitDataSchema, bot_token_bytes: bytes) -> bool:
    parsed_data = init_data.parsed_init_data_dict
    parsed_data.pop("hash")
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=bot_token_bytes, digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return init_data.hash == calculated_hash


def build_token(user: TgUser) -> str:
    return jwt.encode(
        payload={
            "tg_id": user.tg_id,
        },
        key=settings.JWT_PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> str:
        return token

def validate_token(token: str, user_tg_id: int) -> dict:
    if settings.TESTING:
        return {"tg_id": user_tg_id}
    try:
        payload = jwt.decode(token, settings.JWT_PRIVATE_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.DecodeError:
        raise HttpError(status_code=401, message="Invalid token")
    if payload.get("tg_id") != user_tg_id:
        raise HttpError(status_code=403, message="Forbidden")
    return payload

