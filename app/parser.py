import httpx
from fake_useragent import UserAgent

from config import ADVERTS_URL


class Parser:

    @property
    def headers(self):
        return {
            'User-Agent': UserAgent().random
        }


async def fetch_page(page_number: int = 1):
    _url = ADVERTS_URL
    if page_number > 1:
        _url += f"?page={page_number}"
    async with httpx.AsyncClient() as client:
        response = await client.get(_url)

        if response.status_code == 200:
            return response.content

            print("Got HTML content from page ", page_number)
        else:
            print("Failed to retrieve the web page. Status code:", response.status_code)
