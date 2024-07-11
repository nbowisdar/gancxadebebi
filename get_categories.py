from playwright.sync_api import sync_playwright, Page


def get_url(sub_cat: int) -> str:
    return f"https://gancxadebebi.ge/ru/%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/-1/-{sub_cat}"


def extract_cats_numbers_from_url(url_text: str) -> int:
    sub_cat = url_text.split("/")[-1].split("-")[-1]
    return int(sub_cat)


def check_url(url: str, sub_cat: int) -> bool:
    try:
        real_sub_cat = extract_cats_numbers_from_url(url)
        if real_sub_cat == sub_cat:
            return True
        else:
            print(f"Wrong cat for url: {real_sub_cat =} != {sub_cat = }")
    except Exception:
        print(f"Bad url: {url} for CAT {sub_cat}")
    return False


def work(page: Page) -> list:
    urls = []

    for i in range(1, 250):
        print("Handle page: ", i)
        url = get_url(i)
        page.goto(url)
        if check_url(page.url, i):
            urls.append(page.url)

    return urls


def pars_urls() -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        urls = work(page)
        browser.close()
        return urls


if __name__ == '__main__':
    urls = pars_urls()
    with open("urls.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(urls))
