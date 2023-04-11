from bs4 import BeautifulSoup
import requests
import time
import re
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import PIL.Image
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
from tkinter import ttk

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = PIL.Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def find_items():

    html_text = requests.get(
        'https://www.defacto.com.tr/erkek-jean-ceket').text
    soup = BeautifulSoup(html_text, 'html.parser')
    cards = soup.find_all(
        'div', class_='product-card')
    main_dir = os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop')
    change_rate = ent
    for index, card in enumerate(cards):
        item_card = card.find(
            'div', class_='product-card__image').find('div', class_='image-box').a['href']
        if any(chr.isdigit() for chr in item_card):
            # Item Name
            item_name = card.find('span').text
            # Item Price
            item_price = str(card.find(
                'div', class_='product-card__price--new d-inline-flex').text)
            item_price = re.sub(
                '<[^>]+>', '', item_price).replace(' ', '').replace('TL', '').replace(',', '.')
            # Item Price in Toman
            IR_item_price = (round(change_rate *
                                    (float(correct_price.replace('TL', '').replace(' ', '')))) + 900) // 1000 * 1000
            IR_item_price = '{:,}'.format(IR_item_price)
            # Item Brand
            item_brand = 'DeFacto'
            # Image url
            item_image = card.find('img', class_='lazy swiper-lazy').get('data-srcset').split('jpg')[0]
            image_url = f'https:{item_image}jpg'
            # Download Item Image
            if not os.path.exists(f'{main_dir}\defacto'):
                os.mkdir(f'{main_dir}\defacto')
            img_data = requests.get(image_url, stream=True).content
            with open(f'{main_dir}\defacto\{index}.jpg', 'wb') as handler:
                handler.write(img_data)
            # Edit Image

            my_image = PIL.Image.open(
                    f'{main_dir}/defacto/{index}.jpg')
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
            edit_image.rectangle((1500, 100, 300, 200), fill=('beige'))
            edit_image.text((half_width, 100), text_to_add,
                                ('black'), font=text_price_font)
            edit_image.text((60, (new_height-200)), (f'{item_brand} {item_text}'),
                                ('black'), font=text_title_font)
            # Functions
            my_image.save(
                f'{main_dir}/{page_num}/{index}.jpg')
            # print(f'({index})')
            # print(item_name)
            # print(item_price)
            # print(f'https://defacto.com/{item_card}')
            # print(f'SALE : {sale_notification}')
            # print(f'Second Item sale: {second_sale}')
            # print(f'image URL : {image_url}')
            # if sale_notification:
            #     print(f'before discount : {item_price_sale}')
            # if second_sale:
            #     print(f'second one for : {item_price_sale}')
            # print ('___________')
find_items()
