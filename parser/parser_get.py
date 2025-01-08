import pickle
import asyncio
# from .req_get_wb import superdata
from playwright_my.pwrt_get_wb import superdata
#from playwright_my.s_pwrt_get_wb import superdata


async def parser():
    lst = []
    try:
        with open('items_in_shopping_cart_new.pkl', 'rb') as rpkl:
            my_dict = pickle.load(rpkl)
    except:
        my_dict = {}

    sup: list[dict] = await superdata()

    for item in sup:  # Прогоняем названия товаров
        if item['prices'] <= 0:
            continue
        elif item['keys'] not in my_dict:  # Если это новый товар, то добавляем цены
            my_dict[item['keys']] = {}
            my_dict[item['keys']]['actual_price'] = item['prices']
            my_dict[item['keys']][
                'href'] = f"https://www.wildberries.ru/catalog/{item['keys'].split('-')[0]}/detail.aspx?size={item['size']}"
            my_dict[item['keys']]['min_price'] = item['prices']
            my_dict[item['keys']]['max_price'] = item['prices']
            my_dict[item['keys']]['name'] = item['name']
        elif my_dict[item['keys']]['actual_price'] == item['prices']:
            continue
        elif my_dict[item['keys']]['actual_price'] >= item['prices']:
            lst.append(
                f"""Ура! Товар <b><a href="{my_dict[item['keys']]['href']}">{my_dict[item['keys']]['name']}</a></b> подешевел и теперь стоит <b>{item['prices']}</b> руб. вместо <i>{my_dict[item['keys']]['actual_price']}</i> руб.
    В наличии осталось {item['qty']} шт.
    Самая низкая цена, что я видел раньше была {my_dict[item['keys']]['min_price']}  руб, а максимальная {my_dict[item['keys']]['max_price']}""")

            my_dict[item['keys']]['actual_price'] = item['prices']
            if item['prices'] < my_dict[item['keys']]['min_price']:
                my_dict[item['keys']]['min_price'] = item['prices']
        elif item['prices'] > my_dict[item['keys']]['max_price']:
            my_dict[item['keys']]['max_price'] = item['prices']
            my_dict[item['keys']]['actual_price'] = item['prices']
        elif item['prices'] > my_dict[item['keys']]['actual_price']:
            my_dict[item['keys']]['actual_price'] = item['prices']

    # удаляем из базы товары, которые исчезли из корзины
    #keysinsup = [i['keys'] for i in sup]  # ключи с сайта
    #fordel = [item for item in my_dict if item not in keysinsup]  # список ключей, которые нужно удалить

    #for it in fordel:
     #   del my_dict[it]  # удаление ключей

    with open('items_in_shopping_cart_new.pkl', 'wb') as wpkl:
        pickle.dump(my_dict, wpkl)

    return lst, len(sup)


if __name__ == '__main__':
    parser()
