from bs4 import BeautifulSoup
import requests


html_text = requests.get(
    'https://www.trendyol.com/').text
soup = BeautifulSoup(html_text, 'html.parser')
nav_centers = soup.find('div', class_='sub-nav-center')
for  nav_center in nav_centers:
    headers = nav_center.find_all('li')
    titles = nav_center.find_all('a')
    for title in titles:
        title_t = title.text
    for header in headers:
        text = header.text
        link = header.a['href']
        string=(f"'/{text}\\n'").replace(" ","_")
        print(string)
        # print(f'{link}')
        # print(f'{title_t}')
        # print('-------------------')
