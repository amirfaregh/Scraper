from bs4 import BeautifulSoup
import requests
import time
from python_translator import Translator
import os
translator = Translator()


def find_items():
    change_rate = 2250
    html_text = requests.get(
        'https://www.trendyol.com/sr?q=stradivarius&qt=stradivarius&st=stradivarius&os=1').text
    soup = BeautifulSoup(html_text, 'lxml')
    cards = soup.find_all('div', class_='p-card-chldrn-cntnr card-border')

    for index, card in enumerate(cards):

        # Item Title
        item_name = card.find(
            'span', class_='hasRatings')
        if item_name is not None:
            item_text = item_name.text
        else:
            item_text = "NoneType"
            index = "Error"
        # Item title in Farsi
        item_name_PR = translator.translate(item_text, "persian", "turkish")
        # Item Price
        TL_item_price = card.find(
            'div', 'prc-box-dscntd').text.replace(',', '.')
        # Item Prize in Toman
        IR_item_price = change_rate * \
            (float(TL_item_price.replace('TL', '').replace(' ', '')))
        # Item Brand
        item_brand = card.find('span', class_='prdct-desc-cntnr-ttl').text
        # Item Link
        item_link = card.a['href']
        # Item Image Link
        item_html_text = requests.get(
            'http://www.trendyol.com'+item_link).text
        item_soup = BeautifulSoup(item_html_text, 'lxml')
        image_url = item_soup.find_all('img', loading='lazy')[0]['src']
        # Download Item Image
        img_data = requests.get(image_url, stream=True).content
        with open(f'posts/Trendyol/Erkek/{index}.jpg', 'wb') as handler:
            handler.write(img_data)
            # print(type(img_data))
        with open(f'posts/Trendyol/Erkek/{index}.txt', 'w', encoding="utf-8") as f:
            f.write(f"item name: {item_text}\n")
            f.write(f"item name: {item_name_PR}\n")
            f.write(f"item price in TL: {TL_item_price}\n")
            f.write(f"item price in IR: {IR_item_price}\n")
            f.write(f"item brand: {item_brand}\n")
            f.write(f"item address: http://www.trendyol.com{item_link}\n")
            f.write(f"picture link: {image_url}\n")
            f.write("_______________________")

    print("files have been created")
    # print(index)
    # print(f"item name: {item_text}")
    # print(f"item name: {item_name_PR}\n")
    # print(f"item price in TL: {TL_item_price}\n")
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
