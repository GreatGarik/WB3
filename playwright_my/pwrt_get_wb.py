import logging
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
        browser = await p.chromium.launch(headless=True, args=[
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-infobars',
        '--disable-extensions',
        '--window-size=1920,1080'
    ])

        # инициализация страницы
        '''
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        '''
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            storage_state='state.json'
        )



        # переход по url адресу:
        page = await context.new_page()
        # Отключение автоматизации
        await page.evaluate("navigator.__proto__.webdriver = undefined")
        await page.goto('https://www.wildberries.ru/lk/basket')
        #await page.wait_for_timeout(5000)
        #await asyncio.sleep(120)
        await page.wait_for_selector('.basket-section__header', timeout=10000)


        await context.storage_state(path='state.json')

        # await page.goto('https://www.wildberries.ru/lk/basket')

        soup = BeautifulSoup(await page.content(), 'html.parser')
        #soup = BeautifulSoup(await page.content(), 'lxml')
        tst = soup.find_all('a', class_="good-info__title j-product-popup")
        rrr = soup.find_all('div', class_="list-item__price-new")

        await browser.close()

        #name_list = [item.text.replace(', ', ' ').strip() for item in tst]
        prices_list = [i.text.replace(u'\xa0', u'').strip('₽') for i in rrr]
        #print(*zip(name_list, prices_list))
        for number, item in enumerate(tst[:len(prices_list)]):

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
