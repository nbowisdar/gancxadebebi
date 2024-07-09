from pydantic import BaseModel, Field


class AdvertInner(BaseModel):
    subcategory: str | None = None
    category: str | None = None
    phone_numbers: list[str | None] = Field(default_factory=list)


class AdvertOuter(BaseModel):
    id: str | None = None
    title: str | None = None
    url: str | None = None
    city: str | None = None
    date: str | None = None

    @staticmethod
    def _to_latin(text: str) -> str:
        return text.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')

    def to_latin(self):
        if self.id:
            self.id = self._to_latin(self.id)

        if self.title:
            self.title = self._to_latin(self.title)

        if self.url:
            self.url = self._to_latin(self.url)

        if self.city:
            self.city = self._to_latin(self.city)

        if self.date:
            self.date = self._to_latin(self.date)


class AdvertFull(AdvertInner, AdvertOuter):
    pass


"""{
    "city": "Тбилиси",
    "region": "Картли",
    "category": "Недвижимость",
    "subcategory": "Аренда квартир",
    "phone_numbers": ["+995123456789", "+995987654321"]
}"""
