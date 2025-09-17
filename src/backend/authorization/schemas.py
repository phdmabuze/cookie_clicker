import json
import urllib.parse

from ninja import Schema
from pydantic import BaseModel, PrivateAttr


class TelegramUserSchema(BaseModel):
    id: int
    username: str | None = ""
    first_name: str | None = ""
    last_name: str | None = ""
    bio: str | None = ""
    language_code: str | None = None
    is_premium: bool | None = None
    photo_url: str | None = None
    has_restricted_voice_and_video_messages: bool | None = False


class WebAppInitDataSchema(BaseModel):
    auth_date: int
    hash: str | None = None
    user: TelegramUserSchema

    _parsed_init_data_dict: dict = PrivateAttr(None)  # type: ignore

    @property
    def parsed_init_data_dict(self) -> dict:
        if self._parsed_init_data_dict is None:
            raise ValueError("parsed_init_data_dict is not set")
        return self._parsed_init_data_dict

    @classmethod
    def from_str(cls, data: str) -> "WebAppInitDataSchema":
        parsed_data_dict = dict(urllib.parse.parse_qsl(data))
        parsed_data = parsed_data_dict.copy()
        parsed_data["user"] = json.loads(parsed_data_dict["user"])
        i = cls.model_validate(parsed_data)
        i._parsed_init_data_dict = parsed_data_dict
        return i


class LoginDataSchema(Schema):
    init_data: str
