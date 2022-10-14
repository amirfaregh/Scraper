from types import NoneType
from bs4 import BeautifulSoup
import requests
import time
from os.path import basename


def find_items():
    html_text = requests.get(
        'https://www.trendyol.com/erkek').text
    soup = BeautifulSoup(html_text, 'lxml')
    cards = soup.find_all('div', class_='p-card-chldrn-cntnr card-border')
    x = 0

    for index, card in enumerate(cards):
        item_name = card.find(
            'span', class_='hasRatings')
        if item_name is not None:
            item_text = item_name.text
        else:
            item_text = "NoneType"
        item_price = card.find(
            'div', 'prc-box-dscntd').text.replace(' ', ',').replace(',', '.')
        item_brand = card.find('span', 'prdct-desc-cntnr-ttl').text
        item_link = card.a['href']
        x = x+1

        with open(f'posts/Trendyol/Erkek/{index}.txt', 'w', encoding="utf-8") as f:
            f.write(f"item name: {item_text}\n")
            f.write(f"item price: {item_price.strip()}\n")
            f.write(f"item brand: {item_brand}\n")
            f.write(f"item address: http://www.trendyol.com{item_link}\n")
            f.write("_______________________")
    print("files have been created")

    # print(index)
    # print(f"item name: {item_text}")
    # print(f"item price: {item_price.strip()}")
    # print(f"item brand: {item_brand}")
    # print(f"item address: http://www.trendyol.com{item_link}")
    # print('-----------------------')


find_items()

# if __name__ == '__main__':
#     while True:
#         find_items()
#         time_wait = 0.6
#         print(f'Waiting {time_wait} minutes...')
#         time.sleep(time_wait*60)
