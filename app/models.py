from pydantic import BaseModel


class AdvertInner(BaseModel):
    subcategory: str
    category: str
    phone_numbers: list[str]


class AdvertOuter(BaseModel):
    id: str | None
    title: str | None
    url: str | None
    city: str | None
    date: str | None
    # region: str = ""


class AdvertFull(AdvertInner, AdvertOuter):
    pass


"""{
    "city": "Тбилиси",
    "region": "Картли",
    "category": "Недвижимость",
    "subcategory": "Аренда квартир",
    "phone_numbers": ["+995123456789", "+995987654321"]
}"""
