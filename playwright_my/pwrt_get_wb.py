import logging
from time import sleep
from playwright.async_api import async_playwright, expect
from bs4 import BeautifulSoup
import asyncio

'''
async def superdata():
    sup = []

    # открыть соединение
    async with async_playwright() as p:
        # инициализация браузера (без видимого открытия браузера)
        # browser = p.chromium.launch()

        # инициализация браузера (с явным открытием браузера)
        browser = await p.chromium.launch(headless=False, args=[
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-infobars',
        '--disable-extensions',
        '--window-size=1920,1080'
    ])

        # инициализация страницы
        
        #context = await browser.new_context(
        #    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        #)
        
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
        
'''


async def fetch_page_content(page):
    """Переходит на страницу, делает скриншот и возвращает её содержимое."""
    await page.goto('https://www.wildberries.ru/lk/basket')
    # Делаем скриншот
    await page.screenshot(path='basket_screenshot1.png', full_page=True)
    # Ожидание загрузки нужного селектора
    try:
        await page.wait_for_selector('.basket-section__header', timeout=10000)
        # Делаем скриншот
        await page.screenshot(path='basket_screenshot.png', full_page=True)
    except Exception as e:
        logging.error(f"Ошибка при ожидании селектора: {e}")
    return await page.content()


async def extract_data(soup):
    """Извлекает данные из HTML."""
    items = []
    product_blocks = soup.find_all('div', class_="accordion__list-item list-item j-b-basket-item")

    for block in product_blocks:
        try:
            # Извлечение названия товара и его ссылки
            item_link = block.find('a', class_="img-plug list-item__good-img") or block.find('a', class_="good-info__title")
            name = item_link.text.replace(', ', ' ').strip() if item_link else 'Не задано'
            cod1s = item_link.get('href').split('/')[4] if item_link else 'Не задано'
            characteristicid = item_link.get('href').split('=')[-1] if item_link else 'Не задано'

            # Извлечение цен
            price_divs = block.find_all('div', class_="list-item__price-new")
            prices = [int(price_div.text.replace(u'\xa0', '').strip('₽')) for price_div in price_divs if
                      price_div.text.replace(u'\xa0', '').strip('₽').isdigit()]

            # Выбор минимальной цены, если она есть
            price = min(prices) if prices else 0

            items.append({
                'keys': f"{cod1s}-{characteristicid}",
                'name': name,
                'prices': price,
                'qty': 5,
                'size': characteristicid
            })
        except (ValueError, KeyError) as e:
            logging.error(f"Ошибка при извлечении данных: {e}")

    return items

async def superdata():
    sup = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--disable-extensions',
            '--window-size=1920,1080'
        ])
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            storage_state='state.json'
        )
        page = await context.new_page()
        await page.evaluate("navigator.__proto__.webdriver = undefined")

        try:
            content = await fetch_page_content(page)
            soup = BeautifulSoup(content, 'html.parser')
            sup = await extract_data(soup)
            await context.storage_state(path='state.json')
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
        finally:
            await browser.close()

    return sup


if __name__ == "__main__":
    asyncio.run(superdata())
