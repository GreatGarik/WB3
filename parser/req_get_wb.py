import requests
import json
import ast
from ids import cookies, headers

def superdata() -> list:
    '''
    response = requests.post('https://ru-basket-api.wildberries.ru/lk/basket/items', cookies=cookies, headers=headers)
    my_dict = json.loads(response.text)

    data = {}

    for num, item in enumerate(my_dict['value']):
        data[f'basketItems[{num}][chrtId]'] = my_dict['value'][num]['characteristicId']
        data[f'basketItems[{num}][quantity]'] = my_dict['value'][num]['quantity']
        data[f'basketItems[{num}][cod1S]'] = my_dict['value'][num]['cod1S']
        data[f'basketItems[{num}][targetUrl]'] = my_dict['value'][num]['targetUrl']


    '''

    with open('items.txt') as datafile:
        data = datafile.read()
        # data = ast.literal_eval(text)


    params = ''

    response = requests.post(
        'https://ru-basket-api.wildberries.ru/webapi/lk/basket/data',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    answer = json.loads(response.text)

    sup = []

    for item in answer['value']['data']['basket']['basketItems']:
        sto = [i['qty'] for i in item['stocks']]  # Считаем количество на складах
        try:
            sup.append({'keys': str(item['cod1S']) + '-' + str(item['characteristicId']),
                        'name': item['goodsName'] + ' ' + item['brandName'],
                        'prices': item['priceWithCouponAndDiscount'], 'qty': sum(sto),
                        'size': str(item['characteristicId'])})
        except KeyError:
            pass

    return sup


if __name__ == '__main__':
    superdata()
