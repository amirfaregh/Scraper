from bs4 import BeautifulSoup
import requests
import re
import os
from PIL import Image, ImageDraw, ImageFont

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def find_items():
    html_text = requests.get('https://www.defacto.com.tr/kadin-bluz').text
    soup = BeautifulSoup(html_text, 'html.parser')
    cards = soup.find_all('div', class_='product-card')
    main_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    change_rate = 3300

    for index, card in enumerate(cards):
        item_card = card.find('div', class_='product-card__image').find('div', class_='image-box').a['href']
        # Item Name
        item_name = card.find('span').text
        # Item Price
        item_price = str(card.find('div', class_='product-card__price--new d-inline-flex').text)
        item_price = re.sub('<[^>]+>', '', item_price).replace(' ', '').replace('TL', '').replace(',', '.')
        # Item Price in Toman
        IR_item_price = (round(change_rate * (float(item_price.replace('TL', '').replace(' ', '')))) + 900) // 1000 * 1000
        IR_item_price = '{:,}'.format(IR_item_price)
        # Item Brand
        item_brand = 'DeFacto'
        # Image url
        item_image = card.find('img', class_='lazy swiper-lazy').get('data-srcset').split('jpg')[0]
        image_url = f'https:{item_image}jpg'
        print(index)
        print(item_card)
        print(item_name)
        print(item_price)
        print(image_url)
        print('_________')
        # # Download Item Image
        # if not os.path.exists(os.path.join(main_dir, 'defacto')):
        #     os.mkdir(os.path.join(main_dir, 'defacto'))
        # img_path = os.path.join(main_dir, 'defacto', f'{index}.jpg')
        # with open(img_path, 'wb') as handler:
        #     handler.write(requests.get(image_url, stream=True).content)

        # # Edit Image
        # my_image = Image.open(img_path)
        # my_image = add_margin(my_image, 250, 100, 250, 100, 'white')

        # # Parameters
        # text_price_size = 80
        # text_title_size = 30
        # text_price_font = ImageFont.truetype(
        #     "arial.ttf", text_price_size)
        # text_title_font = ImageFont.truetype(
        #     "arial.ttf", text_title_size)

        # text_to_add = (f"Toman  {IR_item_price}")
        # edit_image = ImageDraw.Draw(my_image)
        # width, height = my_image.size
        # half_width = (width/3)-(text_price_size)
        # new_height = height-20
        # edit_image.rectangle((1500, 100, 300, 200), fill=('beige'))
        # edit_image.text((half_width, 100), text_to_add,
        #                     ('black'), font=text_price_font)
        # edit_image.text((60, (new_height-200)), (f'{item_brand}'),
        #                     ('black'), font=text_title_font)
        # # Functions
        # my_image.save(
        #     f'{main_dir}/{page_num}/{index}.jpg')


find_items()
