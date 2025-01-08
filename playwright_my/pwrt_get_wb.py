from time import sleep
import json
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
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])

        # инициализация страницы
        context = await browser.new_context(storage_state='state.json', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')


        # переход по url адресу:
        page = await context.new_page()
        await page.goto('https://ozon.ru/cart')
        for i in range(0, 2000, 100):  # Прокрутка на 5000 пикселей с шагом 100
            await page.evaluate(f'window.scrollBy(0, {i})')
            await asyncio.sleep(0.2)  # Задержка между прокрутками
        #await asyncio.sleep(30)
        await page.wait_for_timeout(600)
        # await context.storage_state(path='state.json')

        # await page.goto('https://www.wildberries.ru/lk/basket')
        await context.storage_state(path='state.json')

        soup = BeautifulSoup(await page.content(), 'html.parser')
        #soup = BeautifulSoup(await page.content(), 'lxml')
        #all_links = soup.find_all('div', class_="d4019-a iu_23")
        all_links = soup.find('div', id='state-controls-1436757-default-1')
        all_prices = soup.find_all('span', class_="c3023-a1 tsHeadline400Small c3023-b1 c3023-a5")
        all_names = soup.find_all('div', class_="bq010-a bq010-a4 bq010-a7 b9d_4_6")
        await browser.close()

        #name_list = [item.text.replace(', ', ' ').strip() for item in tst]
        #all_links = [i.get('favlistslink') for i in all_links]
        if all_links:
            data_state = all_links['data-state']

            # Преобразуем строку в словарь
            data_dict = json.loads(data_state)
            # Извлекаем массив идентификаторов из postBody
            post_body = data_dict['deleteButtonWeb']['action']['params']['postBody']

            # Преобразуем строку JSON в словарь
            post_body_dict = json.loads(post_body)

            # Извлекаем массив идентификаторов
            all_links = json.loads(post_body_dict['params'])['items']


        prices_list = [i.text.replace(u'\u2009', u'').strip('₽') for i in all_prices]
        all_names = [i.text.strip() for i in all_names]
        #print(*zip(name_list, prices_list))
        for number, item in enumerate(all_links[:len(prices_list)]):

            #cod1s: str = item.get('href').split('/?')[0]
            #cod1s: str = cod1s.split('-')[-1]
            #characteristicid: str = item.get('href').split('/')[-1]
            #name: str = item.text.replace(', ', ' ').strip()
            sto: int = 5 # заглушка
            try:
                sup.append({'keys': item,
                            'name': all_names[number],
                            'prices': int(prices_list[number]),
                            'qty':sto})
                            #'size': characteristicid})
            except KeyError:
                pass
        # cookies = await context.cookies()
        # сделать скриншот
        # print(cookies)
        print(sup)
        return sup


if __name__ == "__main__":
    asyncio.run(superdata())
