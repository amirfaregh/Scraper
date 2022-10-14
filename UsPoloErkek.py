from types import NoneType
from bs4 import BeautifulSoup
import requests
import time
from os.path import basename


def find_items():
    html_text = requests.get(
        'https://tr.uspoloassn.com/erkek-tum-urunler/').text
    soup = BeautifulSoup(html_text, 'html.parser')
    cards = soup.find_all('div', class_='product__listing--content')

    for index, card in enumerate(cards):

        item_name = (card.find(class_='product__name')).a.text

        item_price_group = card.find(
            'div', class_='product__listing--basket-price')
        item_price = item_price_group.find(
            'span').text.replace(',', '.').replace(' TL', '')

        item_brand = 'UsPolo'

        item_link = card.find('span').a['href']

        # print(index)
        # print(f"item name: {item_name}")
        # print(f"item price: {item_price}")
        # print(f"item brand: {item_brand}")
        # print(f"item address: https://tr.uspoloassn.com/{item_link}")
        # print('-----------------------')

        with open(f'posts/UsPolo/Erkek/{index}.txt', 'w', encoding="utf-8") as f:
            f.write(f"item name: {item_name}\n")
            f.write(f"item price: {item_price}\n")
            f.write(f"item brand: {item_brand}\n")
            f.write(f"item address: https://tr.uspoloassn.com{item_link}\n")
            f.write("_______________________")
    print("files have been created")


find_items()
