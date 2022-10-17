from bs4 import BeautifulSoup
import requests
import time


def find_items():

    html_text = requests.get(
        'https://www.mavi.com/kadin/c/1?q=:topRated').text
    soup = BeautifulSoup(html_text, 'html.parser')
    cards = soup.find_all('div', class_='product-item')
    item_name = cards.find(class_='product-title')
    print(item_name)


find_items()
