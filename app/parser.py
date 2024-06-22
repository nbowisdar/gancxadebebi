import httpx
from fake_useragent import UserAgent

from config import ADVERTS_URL


class Parser:

    @property
    def headers(self):
        return {
            'User-Agent': UserAgent().random
        }

    async def fetch_page(self, page_number: int = 1) -> tr:
        _url = ADVERTS_URL
        if page_number > 1:
            _url += f"?page={page_number}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(_url)
            if response.status_code == 200:
                print("Got HTML content from page ", page_number)
                return response.content
            raise Exception("Failed to retrieve the web page. Status code:", response.status_code)
