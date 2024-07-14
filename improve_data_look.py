import json
import urllib.parse
import re
from pprint import pprint

# Define a mapping of month names in Russian to month numbers
month_mapping = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12"
}


# Clean and format the date
def clean_date(date_str) -> str:
    # Remove leading and trailing whitespace
    date_str = date_str.strip()
    # Extract day, month, and year from the date string
    match = re.match(r"(\d+)\s+(\w+)\s+(\d+)", date_str)
    if match:
        day, month_word, year = match.groups()
        month = month_mapping.get(month_word.lower())
        if month:
            return f"{day.zfill(2)}.{month}.{year}"
    return date_str


data = [{
    "id": "GEO1439762",
    "title": "Продаю 4-х комнатную чешскую квартиру в Санзоне.",
    "url": "https://gancxadebebi.ge/ru/%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/%D0%9D%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C-1/%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B0-%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8-1/%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D1%8E-4-%D1%85-%D0%BA%D0%BE%D0%BC%D0%BD%D0%B0%D1%82%D0%BD%D1%83%D1%8E-%D1%87%D0%B5%D1%88%D1%81%D0%BA%D1%83%D1%8E-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83-%D0%B2-%D0%A1%D0%B0%D0%BD%D0%B7%D0%BE%D0%BD%D0%B5--GEO1439762",
    "city": "Самцхе-Джавахети >> Боржоми",
    "date": "\n25 декабря 2023\n",
    "subcategory": None,
    "category": None,
    "phone_numbers": [
        "(+995) 595 50 78 83, (+995) 032 219 46 53"
    ]
}, ]


def improve_one(data: dict):
    # Categories
    url = urllib.parse.unquote(data["url"])
    x = url.split("/")
    cat = x[-3]
    sub_cat = x[-2]
    data["category"] = cat
    data["subcategory"] = sub_cat

    # City
    if ">>" in data["city"]:
        region, city = data["city"].split(">>")
        data["region"] = region.strip()
        data["city"] = city.strip()
        if not region and city == "Тбилиси":
            data["region"] = "Тбилиси"
        else:
            data["region"] = None

    better_phones = []
    for phones in data["phone_numbers"]:
        if phones:
            for phone in phones.split(","):
                bettee_phone = phone.replace(")", "").replace("(", "").replace(" ", "").replace("-", "")
                if bettee_phone.isdigit():
                    if len(bettee_phone) == 9:
                        bettee_phone = f"+995{bettee_phone}"
                    if len(bettee_phone) == 13:
                        better_phones.append(bettee_phone)

    data["phone_numbers"] = better_phones
    data["date"] = clean_date(data["date"])


def main():
    with open('results/full_data_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        c = 0
        for d in data:
            c += 1
            improve_one(d)
            print(f"Improved {c} out of {len(data)}")

    with open('full_data_all_improved.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
    # for d in data:
    #     improve_one(d)
