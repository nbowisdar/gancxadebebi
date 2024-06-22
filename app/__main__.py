import httpx

from config import ADVERTS_URL


async def fetch_pages(page_number: int = 1):
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

# async def main():


# Usage example
import asyncio

url = "https://gancxadebebi.ge/ru/%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/Green-Budapest-GEO1491588"
file_path = 'output.html'  # replace with your desired output file path

asyncio.run(fetch_and_save_html(url, file_path))
