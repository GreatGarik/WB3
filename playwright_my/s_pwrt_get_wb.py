from time import sleep
from playwright.sync_api import sync_playwright, expect
from bs4 import BeautifulSoup

def superdata() -> list:
    sup = []

    # открыть соединение
    with sync_playwright() as p:
        # инициализация браузера (без видимого открытия браузера)
        # browser = p.chromium.launch()

        # инициализация браузера (с явным открытием браузера)
        browser = p.chromium.launch(channel='chrome', headless=False)

        # инициализация страницы

        #context = browser.new_context()
        context = browser.new_context(storage_state='state.json')

        # переход по url адресу:
        page = context.new_page()
        page.goto('https://www.wildberries.ru/lk/basket')
        page.wait_for_timeout(5000)
        # await context.storage_state(path='state.json')


        # await page.goto('https://www.wildberries.ru/lk/basket')

        soup = BeautifulSoup(page.content(), 'html.parser')
        #soup = BeautifulSoup(await page.content(), 'lxml')
        tst = soup.find_all('a', class_="good-info__title j-product-popup")
        rrr = soup.find_all('div', class_="list-item__price-new wallet")
        browser.close()

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
                            'prices': prices_list[number],
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
    print(superdata())
