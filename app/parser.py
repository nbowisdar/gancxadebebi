import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import AsyncGenerator

import httpx
from fake_useragent import UserAgent
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from app.extractor import extract_data_from_inner_page
from app.models import AdvertOuter, AdvertFull
from config import MAX_PAGES, ADVERTS_URL, HEADLESS_BROWSER


@dataclass
class PageManager:
    context: BrowserContext
    ready_pages: list[Page] = field(default_factory=list)
    busy_pages: list[Page] = field(default_factory=list)
    is_ready = False

    async def start(self, page_amount: int = MAX_PAGES):
        print(f"Opening {page_amount} pages...")
        for _ in range(page_amount):
            page = await self.context.new_page()
            self.ready_pages.append(page)
        print(f"Opened {page_amount} pages")
        self.is_ready = True

    def release_page(self, page: Page):
        print(self.busy_pages, page)
        self.busy_pages.remove(page)
        self.ready_pages.append(page)

    def get_page(self) -> Page:
        page = self.ready_pages.pop()
        self.busy_pages.append(page)
        return page

    async def visit_page(self, advert: AdvertOuter) -> AdvertFull:
        if not self.is_ready:
            raise Exception("Pages are not ready")
        if not self.ready_pages:
            # print("Too many pages are busy. Waiting...")
            await asyncio.sleep(1)
            return await self.visit_page(advert)
        page = self.get_page()
        print(f"Visiting {advert.url}...")
        await page.goto(advert.url)
        await page.wait_for_load_state("domcontentloaded")
        content = await page.content()
        print(f"Got HTML content from {advert.url}")

        self.release_page(page)

        data = extract_data_from_inner_page(content)
        full = AdvertFull(**data.dict(), **advert.dict())
        full.to_latin()
        # print(full.dict())
        return full

    def clear(self):
        self.ready_pages.clear()
        self.busy_pages.clear()


class Parser:
    context: BrowserContext
    page_manager: PageManager
    is_active: bool = False

    def __init__(self, browser: Browser):
        self.browser = browser

    @property
    def headers(self):
        return {
            'User-Agent': UserAgent().random
        }

    async def start(self):
        context = await self.browser.new_context(
            java_script_enabled=True
        )
        self.page_manager = PageManager(context)
        await self.page_manager.start()

    async def run(self, adverts: list[AdvertOuter]):

        # Run tasks concurrently
        tasks = []
        for adv in adverts:
            tasks.append(
                self.page_manager.visit_page(adv)
            )
        result = await asyncio.gather(*tasks)
        time.sleep(2)
        return result

    async def fetch_outer_page(self, page_number: int = 1) -> str | None:
        _url = ADVERTS_URL
        if page_number > 1:
            _url += f"?page={page_number}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(_url)
            if response.status_code == 200:
                print("Got HTML content from page ", page_number)
                return str(response.content)
            print("Failed to retrieve the web page. Status code:")


@asynccontextmanager
async def get_parser() -> AsyncGenerator[Parser, None]:
    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.launch(headless=HEADLESS_BROWSER)
            parser = Parser(browser)
            await parser.start()
            yield parser
        finally:
            await browser.close()


async def pars_inner_page(urls: list[str]):
    async with get_parser() as parser:
        await parser.run(urls)


async def main():
    urls = [
        'https://gancxadebebi.ge/ru/%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/Green-Budapest-GEO1491588',
        'https://gancxadebebi.ge/ru/%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%B4%D1%83%D1%85%D0%BE%D0%B2%D0%BA%D0%B0-%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D0%B4%D1%83%D1%85%D0%BE%D0%B2%D0%BA%D0%B0-%D0%BF%D0%B5%D1%87%D1%8C-%D0%B6%D0%B0%D1%80%D0%BE%D1%87%D0%BD%D1%8B%D0%B9-%D1%88%D0%BA%D0%B0%D1%84-%D1%85%D0%BB%D0%B5%D0%B1%D0%BE%D0%BF%D0%B5%D1%87%D0%BA%D0%B0-220-%D0%92-950-%D0%92%D1%82-0-95-%D0%BA%D0%92%D1%82-%D0%A1%D0%A1%D0%A1%D0%A0-USSR-GEO1490693',
    ]
    await pars_inner_page(urls)


if __name__ == '__main__':
    asyncio.run(main())
