import os
import shutil
import time
from ast import main
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import PIL.Image
from python_translator import Translator
from tkinter import *


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = PIL.Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def black_friday():
    main_dir = (
        f'F:/exercise/scraper/posts/Trendyol/Black friday/')
    if os.path.exists(main_dir):
        shutil.rmtree(main_dir)
        os.mkdir(main_dir)
    else:
        os.mkdir(main_dir)
    os.startfile(main_dir)

    for page_num in range(1, 2):
        web_address = 'https://www.trendyol.com/sr?rb=4925%2C4951%2C2686%2C4869%2C2685&tag=kirmizi_kampanya_urunu%2Cturuncu_kampanya_urunu%2Csari_kampanya_urunu'
        html_text = requests.get(
            f'{web_address}').text
        soup = BeautifulSoup(html_text, 'html.parser')
        translator = Translator()
        change_rate = 2400
        soup = BeautifulSoup(html_text, 'html.parser')
        cards = soup.find_all(
            'div', class_='p-card-chldrn-cntnr card-border')

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
            IR_item_price = (round(change_rate *
                                   (float(correct_price.replace('TL', '').replace(' ', '')))) + 90) // 100 * 100
            IR_item_price = '{:,}'.format(IR_item_price)
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
            item_soup = BeautifulSoup(item_html_text, 'html.parser')
            image_url = item_soup.find_all('img', loading='lazy')[0]['src']
            # __________________________________
            if not os.path.exists(main_dir+'/'+str(page_num)):
                os.mkdir(f'{main_dir}/{page_num}')
            else:
                pass
            # __________________________________

            # Make sub directory

            # if not os.path.exists(main_dir+'/'+str(page_num)+'/'+str(index)):
            #     os.mkdir(f'{main_dir}/{page_num}/{index}')
            # else:
            #     pass
            # __________________________________

            # Download Item Image

            img_data = requests.get(image_url, stream=True).content
            with open(f'{main_dir}/{page_num}/{index}.jpg', 'wb') as handler:
                handler.write(img_data)
            # __________________________________

            # Edit Image

            my_image = PIL.Image.open(
                f'{main_dir}/{page_num}/{index}.jpg')
            my_image = add_margin(my_image, 250, 100, 250, 100, 'white')

            # Parameters
            text_price_size = 80
            text_title_size = 30
            text_price_font = ImageFont.truetype(
                "arial.ttf", text_price_size)
            text_title_font = ImageFont.truetype(
                "arial.ttf", text_title_size)

            text_to_add = (f"Toman  {IR_item_price}")
            edit_image = ImageDraw.Draw(my_image)
            width, height = my_image.size
            half_width = (width/3)-(text_price_size)
            new_height = height-20
            # Edits
            edit_image.rectangle((1500, 100, 300, 200), fill=('beige'))
            edit_image.text((half_width, 100), text_to_add,
                            ('black'), font=text_price_font)
            edit_image.text((60, (new_height-200)), (f'{item_brand} {item_text}'),
                            ('black'), font=text_title_font)
            # Functions
            my_image.save(
                f'{main_dir}/{page_num}/{index}.jpg')

            # __________________________________

            with open(f'{main_dir}/{page_num}/{index}/{index}.txt', 'w', encoding="utf-8") as f:
                f.write(f"item name: {item_text}\n")
                f.write(f"item name: {item_name_PR}\n")
                f.write(f"item price in TL: {correct_price}\n")
                f.write(f"item price in IR: {IR_item_price}\n")
                f.write(f"item brand: {item_brand}\n")
                f.write(
                    f"item address: http://www.trendyol.com{item_link}\n")
                f.write(f"picture link: {image_url}\n")
                f.write("_______________________")
            os.remove(f'{main_dir}/{page_num}/{index}.jpg')
            # __________________________________
black_friday()
