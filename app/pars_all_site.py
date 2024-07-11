"""Content Very similar to the content of the __main__.py script."""

import asyncio
import json
import shutil
import time
from urllib.parse import quote

import httpx

from app.extractor import extract_data_from_outer_page
from app.parser import get_parser
from config import RESULT_DIR, BASE_DIR


def save_data_to_file(data: dict | list, url: str, page_number: int):
    sub_dir = RESULT_DIR / url.split("-")[-1]
    sub_dir.mkdir(exist_ok=True)

    file_name = f"page_{page_number}.json"
    with open(sub_dir / file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_data_to_db(data: dict | list):
    url = 'https://example.com/api'

    headers = {
        'Content-Type': 'application/json'
    }
    response = httpx.post(url, json=data, headers=headers)

    # TODO finish it


async def pars_one_url_cat(url: str):
    async with get_parser(url) as parser:
        c = 1
        start_time_main = time.perf_counter()
        while True:
            print("Fetching page ", c)
            content = await parser.fetch_outer_page(c)
            if not content:
                print('All data collected with url: ', url)
                break
            data = extract_data_from_outer_page(content)
            start = time.perf_counter()
            data = await parser.run(data)
            # data = await parser.run([data[0]])

            json_data = [m.dict() for m in data]
            save_data_to_file(json_data, url, c)

            # TODO save data to the db when url will be ready
            # save_data_to_db(json_data)
            c += 1
        print(f"Finished in {time.perf_counter() - start_time_main:.2f} seconds")


async def main():
    shutil.rmtree(RESULT_DIR)
    RESULT_DIR.mkdir()
    time_pars_all_site = time.perf_counter()
    with open(BASE_DIR / "test.txt") as f:
        urls = f.readlines()
        for url in urls:
            encoded_url = quote(url.strip(), safe=':/')
            print("Parsing: ", encoded_url)
            await pars_one_url_cat(encoded_url)

    elapsed_time = time.perf_counter() - time_pars_all_site
    print(f"All parsing completed in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
