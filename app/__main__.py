import asyncio
import json
from pprint import pprint

import httpx

from app.parser import Parser, get_parser
from app.extractor import extract_data_from_outer_page
from config import ADVERTS_URL


async def main():
    async with get_parser() as parser:
        c = 1
        while True:
            print("Fetching page ", c)
            content = await parser.fetch_outer_page(c)
            if not content:
                print('All data collected')
                break
            data = extract_data_from_outer_page(content)
            data = await parser.run(data)
            # data = await parser.run([data[0]])

            json_data = [m.dict() for m in data]
            with open("test_data.json", 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            # for i in data:
            #     pprint(i.dict())
            return
            c += 1


file_path = 'output.html'  # replace with your desired output file path

if __name__ == '__main__':
    asyncio.run(main())
