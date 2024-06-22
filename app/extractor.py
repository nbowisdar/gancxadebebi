from bs4 import BeautifulSoup

from app.models import AdvertBase


def _get_number(soup: BeautifulSoup) -> str:
    return soup.find(class_="cc").text


def _get_category_and_subcategory(soup: BeautifulSoup) -> tuple[str, str]:
    category, subcategory = soup.find(class_="asr").text.split(" >> ")
    return category, subcategory


def extract_data_from_page(html_content: str) -> AdvertBase:
    soup = BeautifulSoup(html_content, 'html.parser')
    number = _get_number(soup)
    category, subcategory = _get_category_and_subcategory(soup)

    return AdvertBase(
        category=category,
        subcategory=subcategory,
        phone_numbers=[number]
    )


def get_city(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find(class_="av").text


def get_data(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find(class_="ad").text


if __name__ == '__main__':
    with open('output2.html', 'r', encoding='utf-8') as file:
        content = file.read()
    data = extract_data_from_page(content)
    print(data.dict())
