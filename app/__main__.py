import asyncio
from pprint import pprint

import httpx

from app.parser import Parser, get_parser
from app.extractor import extract_data_from_outer_page
from config import ADVERTS_URL


async def main():
    async with get_parser() as parser:
        content = await parser.fetch_outer_page(1)
        data = extract_data_from_outer_page(content)
        data = await parser.run([data[0]])

        # pprint(data)
        for i in data:
            pprint(i.dict())


file_path = 'output.html'  # replace with your desired output file path

if __name__ == '__main__':
    asyncio.run(main())
