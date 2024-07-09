import asyncio
import json
import time

import httpx
import schedule

from app.extractor import extract_data_from_outer_page
from app.parser import get_parser
from config import RESULT_DIR


def save_data_to_file(data: dict | list, page_number: int):
    file_name = f"page_{page_number}.json"
    with open(RESULT_DIR / file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_data_to_db(data: dict | list):
    url = 'https://example.com/api'

    headers = {
        'Content-Type': 'application/json'
    }
    response = httpx.post(url, json=data, headers=headers)

    # TODO finish it


async def main():
    async with get_parser() as parser:
        c = 1
        print("Starting...")
        start_time_main = time.perf_counter()
        while True:
            print("Fetching page ", c)
            content = await parser.fetch_outer_page(c)
            if not content:
                print('All data collected')
                break
            data = extract_data_from_outer_page(content)
            start = time.perf_counter()
            data = await parser.run(data)
            # data = await parser.run([data[0]])

            json_data = [m.dict() for m in data]
            save_data_to_file(json_data, c)

            # TODO save data to the db when url will be ready
            # save_data_to_db(json_data)
            c += 1
            print(
                f"DONE CYCLE {c} with adverts {len(json_data)}\n"
                f"Took Finished in {time.perf_counter() - start:.2f} seconds"
            )
        print(f"Finished in {time.perf_counter() - start_time_main:.2f} seconds")


def execute_script():
    asyncio.run(main())


def start():
    # Run first time
    execute_script()

    schedule.every(1).hours.do(execute_script)
    while True:
        print("Running...")
        schedule.run_pending()
        # sleep for 1 second as shown in the documentation
        time.sleep(1)


if __name__ == '__main__':
    start()
