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
import tkinter.messagebox
from tkinter.ttk import *
from tkinter import ttk
from fpdf import FPDF

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = PIL.Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def selection():
    if len(price_entry.get()) == 0:
        tkinter.messagebox.showinfo("ERROR", "Enter Exchange rate")
    else:
        main_dir = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')
        if os.path.exists(main_dir):
            shutil.rmtree(main_dir)
            os.mkdir(main_dir)
        else:
            os.mkdir(main_dir)
        os.startfile(main_dir)
        change_rate = int(price_entry.get())

        for page_num in range(1, 2):
            if len(link_entry.get()) == 0:
                web_address = ('http://www.trendyol.com') #+select.get()+sorting.get())
            else:
                web_address = link_entry.get()
            html_text = requests.get(web_address).text
            soup = BeautifulSoup(html_text, 'html.parser')
            translator = Translator()
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
                                       (float(correct_price.replace('TL', '').replace(' ', '')))) + 900) // 1000 * 1000
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

def makePdf():
    main_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    page_num="1"

    pdf=FPDF()
    pdf.set_auto_page_break(0)

    img_list=[x for x in os.listdir(f'{main_dir}/{page_num}')]

    for img in img_list:
        pdf.add_page()
        image=(f'{main_dir}\{page_num}\{img}')
        pdf.image(image)
    
    pdf.output("cataloge.pdf")  

def clicked(value):
    myLabel = Label(root, text=value)
    myLabel.grid(row=2)

def paste():
    global selected
    selected = root.clipboard_get()
    position = link_entry.index(INSERT)
    link_entry.insert(position, selected)

root = Tk()
root.title('Trendyol Pic Graber')
root.iconbitmap('F:\exercise\scraper\icon.ico')
root.geometry("700x300")

input_label = Label(root, text='Enter URL : ')
input_label.grid(column=0, row=0)

link_entry = Entry(root, width=50)
link_entry.grid(column=1, row=0, sticky='w')

price_label = Label(root, text='Enter Exchange rate : ')
price_label.grid(column=0, row=1)

price_entry = Entry(root, width=15, )
price_entry.grid(column=1, row=1, sticky='w')

paste_but = Button(root, text="Paste", command=paste)
start_but = Button(root, text="Start Search Engin", command=selection)
cataloge_but = Button(root, text="create cataloge", command=makePdf)
paste_but.grid(row=0, column=2)
start_but.grid(row=3, column=0)
cataloge_but.grid(row=4, column=0)
# sorting = StringVar()
# sorting.set('/')

# select = StringVar()
# select.set('/')

# SORTS = [
#     ("En düşük fiyat", "?sst=PRICE_BY_ASC"),
#     ("En yüksek fiyat", "?sst=PRICE_BY_DESC"),
#     ("En Çok satanlar", "?sst=BEST_SELLER"),
#     ("En Çok beğenilenler", "?sst=MOST_RATED"),

# ]

# for text, sort in SORTS:
#     Radiobutton(root, text=text, variable=sorting,
#                 value=sort).grid(column=0, sticky='w')


# GROUPS = [
#     ("Elbise", "/elbise-x-c56"),
#     ("Tişört", "/kadin-t-shirt-x-g1-c73"),
#     ("Gömlek", "/kadin-gomlek-x-g1-c75"),
#     ("Kot Pantolon", "/kadin-jean-x-g1-c120"),
#     ("Kot Ceket", "/kot-ceket-y-s12676"),
#     ("Pantolon", "/kadin-pantolon-x-g1-c70"),
#     ("Mont", "/kadin-mont-x-g1-c118"),
#     ("Bluz", "/kadin-bluz-x-g1-c1019"),
#     ("Ceket", "/kadin-ceket-x-g1-c1030"),
#     ("Etek", "/etek-x-c69"),
#     ("Kazak", "/kadin-kazak-x-g1-c1092"),
#     ("Tesettür", "/kadin-tesettur-giyim-x-g1-c81"),
#     ("Büyük Beden", "/kadin-buyuk-beden-x-g1-c80"),
#     ("Topuklu Ayakkabı", "/kadin-topuklu-ayakkabi-x-g1-c107"),
#     ("Sneaker", "/kadin-sneaker-x-g1-c1172"),
#     ("Günlük Ayakkabı", "/kadin-gunluk-ayakkabi-x-g1-c1352"),
#     ("Babet", "/kadin-babet-x-g1-c113"),
#     ("Sandalet", "/kadin-sandalet-x-g1-c111"),
#     ("Bot", "/kadin-bot-x-g1-c1025"),
#     ("Çanta", "/kadin-canta-x-g1-c117"),
#     ("Saat", "/kadin-saat-x-g1-c34"),
#     ("Takı ", "/kadin-taki-mucevher-x-g1-c28"),
#     ("Şapka", "/kadin-sapka-x-g1-c1181"),
#     ("Cüzdan", "/kadin-cuzdan-x-g1-c1032"),
#     ("Pijama Takımı", "/kadin-pijama-takimi-x-g1-c101496"),
#     ("Gecelik", "/kadin-gecelik-x-g1-c62"),
#     ("Sütyen", "/kadin-sutyen-x-g1-c63"),
#     ("İç Çamaşırı Takımları", "/kadin-ic-camasiri-takimlari-x-g1-c104536"),
#     ("Fantezi Giyim", "/kadin-fantezi-giyim-x-g1-c109067"),
#     ("Çorap", "/kadin-corap-x-g1-c1038"),
#     ("Lüks Çanta", "/sr?fl=luks-ve-tasarim-markalarda-en-begenilenler&wc=117&bu=100161"),
#     ("Lüks Giyim", "/sr?fl=luks-ve-tasarim-markalarda-en-begenilenler&wc=82&bu=100161"),
#     ("Lüks Ayakkabı", "/sr?fl=luks-ve-tasarim-markalarda-en-begenilenler&wc=114&bu=100161"),
#     ("Tasarım Giyim", "/sr?fl=luks-ve-tasarim-markalarda-en-begenilenler&wc=82&bu=100160"),
#     ("Tasarım Ayakkabı", "/sr?fl=luks-ve-tasarim-markalarda-en-begenilenler&wc=114&bu=100160"),
#     ("Parfüm", "/parfum-x-c86"),
#     ("Göz Makyajı", "/goz-makyaji-x-c1347"),
#     ("Cilt Bakım", "/cilt-bakimi-x-c85"),
#     ("Saç Bakımı", "/sac-bakimi-x-c87"),
#     ("Makyaj", "/makyaj-x-c100"),
#     ("Ağız Bakım", "/agiz-bakim-x-c101396"),
#     ("Cinsel Sağlık", "/cinsel-saglik-x-c101408"),
#     ("Vücut Bakım", "/vucut-bakimi-x-c1204"),
#     ("Hijyenik Ped", "/hijyenik-ped-x-c101409"),
#     ("Duş Jeli & Kremleri", "/dus-jeli-ve-kremleri-x-c101401"),
#     ("Epilasyon Ürünleri", "/epilasyon-urunleri-x-c104060"),
#     ("Ruj", "/ruj-x-c1156"),
#     ("Güneş Kremi", "/yuz-gunes-kremi-x-c1061"),
#     ("Sweatshirt", "/kadin-spor-sweatshirt-x-g1-c101456"),
#     ("Tişört", "/kadin-spor-t-shirt-x-g1-c101459"),
#     ("Spor Sütyeni", "/kadin-sporcu-sutyeni-x-g1-c1358"),
#     ("Tayt", "/kadin-spor-tayt-x-g1-c101460"),
#     ("Eşofman", "/kadin-esofman-x-g1-c1049"),
#     ("Koşu Ayakkabısı ", "/kadin-spor-ayakkabi-x-g1-c109"),
#     ("Spor Çantası", "/spor-cantasi-x-c1174"),
#     ("Spor Ekipmanları", "/spor-aletleri-x-c104192"),
#     ("Outdoor Ayakkabı", "/kadin-outdoor-ayakkabi-x-g1-c1128"),
#     ("Kar Botu", "/kadin-kar-botu-x-g1-c142587"),
#     ("Outdoor Ekipmanları", "/outdoor-ekipmanlari-x-c104230"),
#     ("Sporcu Besinleri", "/sporcu-besini-supplementler-x-c105131"),
#     ("Sporcu Aksesuarları", "/kadin-sporcu-aksesuarlari-x-g1-c104521"),
# ]

# for text, group in GROUPS:
#     Radiobutton(root, text=text, variable=select,
#                 value=group).grid(column=0, sticky='w')

# Tabs


root.mainloop()
