from pydantic import BaseModel


class AdvertBase(BaseModel):
    subcategory: str
    category: str
    phone_numbers: list[str]


class AdvertFull(AdvertBase):
    region: str = ""
    city: str = ""


"""{
    "city": "Тбилиси",
    "region": "Картли",
    "category": "Недвижимость",
    "subcategory": "Аренда квартир",
    "phone_numbers": ["+995123456789", "+995987654321"]
}"""
