from time import sleep
from playwright.async_api import async_playwright, expect
from bs4 import BeautifulSoup
import asyncio


async def superdata():
    sup = []

    # открыть соединение
    async with async_playwright() as p:
        # инициализация браузера (без видимого открытия браузера)
        # browser = p.chromium.launch()

        # инициализация браузера (с явным открытием браузера)
        browser = await p.chromium.launch(channel='chrome', headless=False)

        # инициализация страницы

        context = await browser.new_context()
        context = await browser.new_context(storage_state='state.json')

        # переход по url адресу:
        page = await context.new_page()
        await page.goto('https://www.wildberries.ru/lk/basket')
        await page.wait_for_timeout(50000)
        #await context.storage_state(path='state.json')

        await page.goto('https://www.wildberries.ru/lk/basket')
        await browser.close()



if __name__ == "__main__":
    asyncio.run(superdata())
