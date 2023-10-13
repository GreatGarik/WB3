import pickle

with open('../items_in_shopping_cart_new.pkl', 'rb') as rpkl:
    my_dict = pickle.load(rpkl)

for item in my_dict:
    print(my_dict[item]['min_price'])
    #print(my_dict[item]['max_price'])
    if my_dict[item]['min_price'] <= 0:
        my_dict[item]['min_price'] = 20000
    #print(my_dict[item]['min_price'])

with open('../items_in_shopping_cart_new.pkl', 'wb') as wpkl:
    pickle.dump(my_dict, wpkl)
