from ast import main
import shutil
from PIL import Image, ImageDraw, ImageFont
import PIL.Image
from bs4 import BeautifulSoup
import requests
import os
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = PIL.Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def scrape():
# Create a session object for the requests
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

    web_address = 'https://www.trendyol.com/erkek-yuruyus-ayakkabisi-x-g2-c101429'
    html_text = session.get(web_address).text
    soup = BeautifulSoup(html_text, 'html.parser')
    change_rate = 3300
    main_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'scraped_images')
    if os.path.exists(main_dir):
        shutil.rmtree(main_dir)
        os.mkdir(main_dir)
    os.startfile(main_dir)
    cards = soup.find_all('div', class_='p-card-chldrn-cntnr card-border')

    # create directory on desktop
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)

    for index, card in enumerate(cards):
        # Item Title
        item_name = card.find('span', class_='hasRatings')
        item_text = item_name.text if item_name else "NoneType"

        # Item Price
        TL_item_price = card.find('div', 'prc-box-dscntd').text.replace(' TL', '').replace('.', '').replace(',', '.')
        IR_item_price = round(change_rate * float(TL_item_price)) + 90
        IR_item_price = '{:,}'.format(IR_item_price)

        # Item Brand
        item_brand = card.find('span', class_='prdct-desc-cntnr-ttl').text

        # Item Link comment
        item_link = card.a['href']

        # Item Image Link
        item_html_text = session.get(f'http://www.trendyol.com{item_link}').text
        item_soup = BeautifulSoup(item_html_text, 'html.parser')
        image_container = item_soup.find('div',class_='gallery-modal-content')
        image_url = image_container.find('img', loading='lazy')['src']

        # Check availability 
        # Find the div containing the size options
        sizes_div = item_soup.find_all("div", {"class": "sp-itm"})
        sizes = str("")

        for size in sizes_div:
            if size.find("span", {"class": "i-alarm"}):
                pass
            else:
                sizes += size.text + " - "


        # Download image and save to folder on desktop
        
        img_data = requests.get(image_url, stream=True).content
        with open(f'{main_dir}/{index}.jpg', 'wb') as handler:
            handler.write(img_data)

        # Edit Image

        my_image = PIL.Image.open(f'{main_dir}/{index}.jpg')
        my_image = add_margin(my_image, 250, 100, 250, 100, 'white')

        # Parameters
        text_price_size = 80
        text_title_size = 30
        text_size_size = 45
        text_price_font = ImageFont.truetype("arial.ttf", text_price_size)
        text_title_font = ImageFont.truetype("arial.ttf", text_title_size)
        text_size_font = ImageFont.truetype("arial.ttf", text_size_size)

        text_to_add = (f"Toman  {IR_item_price}")
        edit_image = ImageDraw.Draw(my_image)
        width, height = my_image.size
        half_width = (width/3)-(text_price_size)
        new_height = height-20
        # Edits
        edit_image.rectangle((1500, 100, 300, 200), fill=('beige'))
        edit_image.text((half_width, 100), text_to_add, ('black'), font=text_price_font)
        edit_image.text((60, (new_height-150)), (f'{item_brand} {item_text}'), ('black'), font=text_title_font)
        edit_image.text((60, (new_height-210)), (f'size: {sizes}'), ('black'), font=text_size_font)

        # Functions
        my_image.save(f'{main_dir}/{index}.jpg')

    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(main_dir) if f.endswith('.jpg') or f.endswith('.png')]

    # Create a new blank image to group the four images
    group_image = Image.new('RGB', (1080, 2020), (255, 255, 255))

    # Iterate through the list of image files and group them into a single image
    for i in range(0, len(image_files), 4):
        # Open each image and paste it into the group image
        for j in range(4):
            if i + j < len(image_files):
                image = Image.open(os.path.join(main_dir, image_files[i+j]))
                image = image.resize((560, 960), Image.ANTIALIAS)
                x = j % 2 * 540
                y = j // 2 * 960 + 150  # add 100 pixels to top margin
                group_image.paste(image, (x, y))

        # Save the group image with a unique name
        group_image.save(os.path.join(main_dir, 'grouped_{}.jpg'.format(i//4)))

        # Reset the group image for the next batch
        group_image = Image.new('RGB', (1080, 2020), (255, 255, 255))
    

scrape()

