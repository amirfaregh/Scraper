from ast import main
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import time
from python_translator import Translator
import os


def find_items_erkek():
    html_text = requests.get(
        'https://www.trendyol.com/sr?wb=37&lc=118&os=1').text
    soup = BeautifulSoup(html_text, 'lxml')
    erkek_headers = soup.find('div', id='sub-nav-2')
    for erkek_header in erkek_headers:
        sub_header = erkek_header.find(
            'div', class_='category-box').find('ul', class_='sub-item-list')
        sub_sub_headers = sub_header.find_all('li')
        for sub_sub_header in sub_sub_headers:
            for page_num in range(10):
                link = (sub_sub_header.a['href'])+'?pi='+(f'{page_num}')
                main_dir = (
                    f'F:/exercise/scraper/posts/Trendyol/Erkek/{sub_sub_header.a.text}')
                if not os.path.exists(main_dir):
                    os.mkdir(main_dir)
                else:
                    pass
                translator = Translator()
                change_rate = 2400
                html_text = requests.get(
                    f'https://www.trendyol.com/{link}').text

                soup = BeautifulSoup(html_text, 'lxml')
                cards = soup.find_all(
                    'div', class_='p-card-chldrn-cntnr card-border')

                category = soup.find_all('div', class_='breadcrumb')
                print(link)
                page_num = page_num + 1

                for div in category:
                    sub_category = (div.find_all(
                        'a', class_='breadcrumb-item'))[1].find('span').text

                # Ceate Directory
                    directory = f'F:/exercise/scraper/posts/Trendyol/{sub_category}'
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    else:
                        pass

                    for index, card in enumerate(cards):
                        # Item Title
                        item_name = card.find(
                            'span', class_='hasRatings')
                        if item_name is not None:
                            item_text = item_name.text
                        else:
                            item_text = "NoneType"
                            index = "Error"
                        # __________________________________
                        # Item title in Farsi
                        item_name_PR = translator.translate(
                            item_text, "persian", "turkish")
                        # __________________________________

                        # Item Price
                        TL_item_price = card.find(
                            'div', 'prc-box-dscntd').text.replace(' TL', '')
                        stripped = TL_item_price.replace('.', '')
                        correct_price = stripped.replace(',', '.')
                        # __________________________________

                        # Item Price in Toman
                        IR_item_price = change_rate * \
                            (float(correct_price.replace(
                                'TL', '').replace(' ', '')))
                        # __________________________________

                        # Item Brand
                        item_brand = card.find(
                            'span', class_='prdct-desc-cntnr-ttl').text
                        # __________________________________

                        # Item Link
                        item_link = card.a['href']
                        # __________________________________

                        # Item Image Link
                        item_html_text = requests.get(
                            'http://www.trendyol.com'+item_link).text
                        item_soup = BeautifulSoup(item_html_text, 'lxml')

                        image_url = item_soup.find_all(
                            'img', loading='lazy')[0]['src']

                        if image_url == "https://cdn.dsmcdn.com//seller-ads/editor/resources/seller-selection-stamp-v14.png":
                            image_url = image_url = item_soup.find_all(
                                'img', loading='lazy')[1]['src']
                        else:
                            pass
                        # __________________________________

                        # Make sub directory

                        if not os.path.exists(main_dir+'/'+str(index)):
                            os.mkdir(f'{main_dir}/{index}')
                        else:
                            pass
                        # __________________________________

                        # Download Item Image

                        # img_data = requests.get(
                        #     image_url, stream=True).content
                        # with open(f'{main_dir}/{index}/{index}.jpg', 'wb') as handler:
                        #     handler.write(img_data)
                        # # __________________________________
                        # with open(f'{main_dir}/{index}/{index}.txt', 'w', encoding="utf-8") as f:
                        #     f.write(f"item name: {item_text}\n")
                        #     f.write(f"item name: {item_name_PR}\n")
                        #     f.write(f"item price in TL: {correct_price}\n")
                        #     f.write(f"item price in IR: {IR_item_price}\n")
                        #     f.write(f"item brand: {item_brand}\n")
                        #     f.write(
                        #         f"item address: http://www.trendyol.com{item_link}\n")
                        #     f.write(f"picture link: {image_url}\n")
                        #     f.write("_______________________")
                    # __________________________________
                    print(
                        f'Erkek {sub_sub_header.a.text} updated at{datetime.now()}')
                    print(sub_sub_header.a.text)


def find_items_kadin():
    html_text = requests.get('https://www.trendyol.com').text
    soup = BeautifulSoup(html_text, 'lxml')
    kadin_headers = soup.find('div', id='sub-nav-1')
    for kadin_header in kadin_headers:
        sub_header = kadin_header.find(
            'div', class_='category-box').find('ul', class_='sub-item-list')
        sub_sub_headers = sub_header.find_all('li')
        for sub_sub_header in sub_sub_headers:
            link = sub_sub_header.a['href']
            main_dir = (
                f'F:/exercise/scraper/posts/Trendyol/Kadin/{sub_sub_header.a.text}')
            if not os.path.exists(main_dir):
                os.mkdir(main_dir)
            else:
                pass
            translator = Translator()
            change_rate = 2400
            html_text = requests.get(
                f'https://www.trendyol.com/{link}').text

            soup = BeautifulSoup(html_text, 'lxml')
            cards = soup.find_all(
                'div', class_='p-card-chldrn-cntnr card-border')

            category = soup.find_all('div', class_='breadcrumb')
            for div in category:
                sub_category = (div.find_all(
                    'a', class_='breadcrumb-item'))[1].find('span').text

            # Ceate Directory
            directory = f'F:/exercise/scraper/posts/Trendyol/{sub_category}'
            if not os.path.exists(directory):
                os.mkdir(directory)
            else:
                pass
                for index, card in enumerate(cards):

                    # Item Title
                    item_name = card.find(
                        'span', class_='hasRatings')
                    if item_name is not None:
                        item_text = item_name.text
                    else:
                        item_text = "NoneType"
                        index = "Error"
                    # __________________________________
                    # Item title in Farsi
                    item_name_PR = translator.translate(
                        item_text, "persian", "turkish")
                    # __________________________________

                    # Item Price
                    TL_item_price = card.find(
                        'div', 'prc-box-dscntd').text.replace(' TL', '')
                    stripped = TL_item_price.replace('.', '')
                    correct_price = stripped.replace(',', '.')
                    # __________________________________

                    # Item Price in Toman
                    IR_item_price = change_rate * \
                        (float(correct_price.replace('TL', '').replace(' ', '')))
                    # __________________________________

                    # Item Brand
                    item_brand = card.find(
                        'span', class_='prdct-desc-cntnr-ttl').text
                    # __________________________________

                    # Item Link
                    item_link = card.a['href']
                    # __________________________________

                    # Item Image Link
                    item_html_text = requests.get(
                        'http://www.trendyol.com'+item_link).text
                    item_soup = BeautifulSoup(item_html_text, 'lxml')
                    image_url = item_soup.find_all(
                        'img', loading='lazy')[0]['src']
                    # __________________________________

                    # Make sub directory
                    if not os.path.exists(main_dir+'/'+str(index)):
                        os.mkdir(f'{main_dir}/{index}')
                    else:
                        pass
                    # __________________________________

                    # Download Item Image

                    img_data = requests.get(image_url, stream=True).content
                    with open(f'{main_dir}/{correct_price}.jpg', 'wb') as handler:
                        handler.write(img_data)
                    # __________________________________
                    with open(f'{main_dir}/{index}/{index}.txt', 'w', encoding="utf-8") as f:
                        f.write(f"item name: {item_text}\n")
                        f.write(f"item name: {item_name_PR}\n")
                        f.write(f"item price in TL: {correct_price}\n")
                        f.write(f"item price in IR: {IR_item_price}\n")
                        f.write(f"item brand: {item_brand}\n")
                        f.write(
                            f"item address: http://www.trendyol.com{item_link}\n")
                        f.write(f"picture link: {image_url}\n")
                        f.write("_______________________")
                    # __________________________________
                print(
                    f'Kadin {sub_sub_header.a.text} updated at{datetime.now()}')

   # if __name__ == '__main__':
    #     while True:
    #         find_items()
    #         time_wait = 0.6
    #         print(f'Waiting {time_wait} minutes...')
    #


find_items_erkek()
# find_items_kadin()
