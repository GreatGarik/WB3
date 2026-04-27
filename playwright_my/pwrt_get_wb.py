import logging
import re
from time import sleep
from playwright.async_api import async_playwright, expect
from bs4 import BeautifulSoup
import asyncio

async def fetch_page_content(page):
    """Переходит на страницу, делает скриншот и возвращает её содержимое."""
    await page.goto('https://www.wildberries.ru/lk/basket')
    # Ожидание загрузки нужного селектора
    try:
        await page.wait_for_selector('.basket-section__header', timeout=10000)
        await asyncio.sleep(90)
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
            item_link = (block.find('a', class_="img-plug list-item__good-img j-product-popup")
                         or block.find('a', class_="good-info__title j-product-popup")
                         or block.find('a', class_="good-info__title"))
            name = item_link.get('title') or ''
            if not name:
                img = item_link.find('img')
                name = img.get('alt') if img and img.get('alt') else ''
            if not name:
                name_span = block.find('span', class_="good-info__good-name")
                name = name_span.get_text(strip=True) if name_span else ''
            if not name:
                name = 'Не задано'
            name = name.replace(', ', ' ').strip()
            cod1s = item_link.get('href').split('/')[4] if item_link else 'Не задано'
            characteristicid = item_link.get('href').split('=')[-1] if item_link else 'Не задано'

            # Извлечение цен — ищем все элементы внутри блока, где может быть цена
            price_elems = block.select(
                '.list-item__price-wallet, .list-item__price-new, .list-item__price')  # расширенный селектор
            prices = []
            for el in price_elems:
                text = el.get_text(separator=' ', strip=True)
                m = re.search(r'(\d[\d\s]*)', text)  # находит число с возможными неразрывными пробелами
                if m:
                    num = int(m.group(1).replace('\xa0', '').replace(' ', ''))
                    prices.append(num)

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
            #await asyncio.sleep(120)
            soup = BeautifulSoup(content, 'html.parser')
            sup = await extract_data(soup)
            #print(sup)
            await context.storage_state(path='state.json')
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
        finally:
            await browser.close()

    return sup


if __name__ == "__main__":
    asyncio.run(superdata())
