from ninja import Schema


class UpgradeSchema(Schema):
    id: int
    name: str
    description: str
    price: int
    income_increase: int
    photo: str | None
    is_purchased: bool
