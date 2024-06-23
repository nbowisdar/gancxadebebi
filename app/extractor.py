from bs4 import BeautifulSoup

from app.models import AdvertInner, AdvertOuter
from config import BASE_URL


def get_or_none(soup: BeautifulSoup, class_: str) -> str | None:
    if element := soup.find(class_=class_):
        return element.text


def _get_number(soup: BeautifulSoup) -> str:
    return soup.find(class_="cc").text


def _get_category_and_subcategory(soup: BeautifulSoup) -> tuple[str, str]:
    category, subcategory = soup.find(class_="asr").text.split(" >> ")
    return category, subcategory


def extract_data_from_inner_page(html_content: str) -> AdvertInner:
    soup = BeautifulSoup(html_content, 'html.parser')
    number = _get_number(soup)
    category, subcategory = _get_category_and_subcategory(soup)

    return AdvertInner(
        category=category,
        subcategory=subcategory,
        phone_numbers=[number]
    )


def _extract_single_outer(soup: BeautifulSoup) -> AdvertOuter:
    if id_ := get_or_none(soup, "ar"):
        url = None
        rel_href = soup.find("a").get("href")
        if rel_href:
            url = BASE_URL + rel_href

        return AdvertOuter(
            id=id_,
            title=get_or_none(soup, "at"),
            url=url,
            city=get_or_none(soup, "av"),
            date=get_or_none(soup, "ad"),
        )


def extract_data_from_outer_page(html_content: str) -> list[AdvertOuter]:
    soup = BeautifulSoup(html_content, 'html.parser')

    adverts = []
    for ul in soup.find_all(class_="ua"):
        adverts.extend(ul.find_all('li'))

    print(len(adverts))
    out_data = []
    for ad in adverts:
        if data := _extract_single_outer(ad):
            out_data.append(data)
    return out_data

if __name__ == '__main__':
    with open('outer.html', 'r', encoding='utf-8') as file:
        content = file.read()
    data = extract_data_from_outer_page(content)
    for d in data:
        print(d.dict())
