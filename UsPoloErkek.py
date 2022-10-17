from bs4 import BeautifulSoup
import requests
import time


def find_items():
    global item_link
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

        item_link = card.find('span', 'product__name').a['href']

    #     with open(f'posts/Trendyol/Erkek/{index}.txt', 'w', encoding="utf-8") as f:
    #         f.write(f"item name: {item_name}\n")
    #         f.write(f"item price: {item_price.strip()}\n")
    #         f.write(f"item brand: {item_brand}\n")
    #         f.write(f"item address: https://tr.uspoloassn.com{item_link}\n")
    #         f.write("_______________________")
    # print("files have been created")

        print(index)
        print(f"item name: {item_name}")
        print(f"item price: {item_price.strip()}")
        print(f"item brand: {item_brand}")
        print(f"item address: https://tr.uspoloassn.com{item_link}")
        print('-----------------------')


find_items()


def item_info():
    new_item_link = "https://tr.uspoloassn.com"+item_link

    html_text = requests.get(new_item_link).text
    selected_part = html_text.find_all('ul', class_='cf')
    print(selected_part)


item_info()
