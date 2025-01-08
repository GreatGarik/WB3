from time import sleep
from playwright.async_api import async_playwright, expect
from bs4 import BeautifulSoup
import asyncio


async def superdata():
    sup = []

    async with async_playwright() as p:
        # Запускаем браузер в обычном режиме с отключением автоматизации
        browser = await p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])

        # Создаем новый контекст с пользовательским агентом
        context = await browser.new_context(storage_state='state.json')

        # Создаем новую страницу
        page = await context.new_page()

        # Переходим на нужный сайт
        await page.goto('https://ozon.ru/cart')

        # Ожидаем 10 секунд
        await asyncio.sleep(60)

        await context.storage_state(path='state.json')

        # Ваши действия со страницей
        # ...

        # Закрываем браузер
        await browser.close()




if __name__ == "__main__":
    asyncio.run(superdata())
