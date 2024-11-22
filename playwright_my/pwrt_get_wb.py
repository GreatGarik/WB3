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
        browser = await p.chromium.launch(headless=True)

        # инициализация страницы

        context = await browser.new_context()
        context = await browser.new_context(storage_state='state.json')

        # переход по url адресу:
        page = await context.new_page()
        await page.goto('https://www.wildberries.ru/lk/basket')
        await page.wait_for_timeout(5000)
        # await context.storage_state(path='state.json')

        # await page.goto('https://www.wildberries.ru/lk/basket')

        soup = BeautifulSoup(await page.content(), 'html.parser')
        #soup = BeautifulSoup(await page.content(), 'lxml')
        all_links = soup.find_all('a', class_="good-info__title")
        all_prices = soup.find_all('div', class_="list-item__price-new")
        await browser.close()

        #name_list = [item.text.replace(', ', ' ').strip() for item in tst]
        prices_list = [i.text.replace(u'\xa0', u'').strip('₽') for i in all_prices]
        #print(*zip(name_list, prices_list))
        for number, item in enumerate(all_links[:len(prices_list)]):

            cod1s: str = item.get('href').split('/')[4]
            characteristicid: str = item.get('href').split('=')[-1]
            name: str = item.text.replace(', ', ' ').strip()
            sto: int = 5 # заглушка
            try:
                sup.append({'keys': cod1s + '-' + characteristicid,
                            'name': name,
                            'prices': int(prices_list[number]),
                            'qty':sto,
                            'size': characteristicid})
            except KeyError:
                pass
        # cookies = await context.cookies()
        # сделать скриншот
        # print(cookies)
        #print(sup)
        return sup


if __name__ == "__main__":
    asyncio.run(superdata())
