from ninja import Schema


class UserInfoSchema(Schema):
    username: str
    photo_url: str | None
    balance: int
    income_per_second: int
