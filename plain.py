import requests
import os
from bs4 import BeautifulSoup


def scrap():
    # Create a session object for the requests
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

    web_address = 'https://www.trendyol.com/erkek-esofman-x-g2-c1049'
    html_text = session.get(web_address).text
    soup = BeautifulSoup(html_text, 'html.parser')
    change_rate = 2400

    cards = soup.find_all('div', class_='p-card-chldrn-cntnr card-border')

    # create directory on desktop
    folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'scraped_images')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

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

        # Find the div containing the size options
        sizes_div = item_soup.find_all("div", {"class": "sp-itm"})
        sizes = ""

        for size in sizes_div:
            if size.find("span", {"class": "i-alarm"}):
                pass
            else:
                sizes += size.text + " "

        # Download image and save to folder on desktop
        dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        main_dir = f'{dir}/1'
        img_data = requests.get(image_url, stream=True).content
        with open(f'{main_dir}/{index}.jpg', 'wb') as handler:
            handler.write(img_data)



        print(index)
        print(f"item name: {item_text}")
        print(f"item price in TL: {TL_item_price}")
        print(f"item price in IR: {IR_item_price}")
        print(f"item brand: {item_brand}")
        print(f"item address: http://www.trendyol.com{item_link}")
        print(f"picture saved to: {folder_path}")
        print(f"available sizes: {sizes}")
        print("_______________________")


scrap()
