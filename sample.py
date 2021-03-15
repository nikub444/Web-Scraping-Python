from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/pomorskie/?search%5Bfilter_enum_rooms%5D%5B0%5D=one'


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


def parse_page(number):
    print(f'Pracuje nad strona numer {number}')
    page = get(f'{URL}&page={number}')
    bs = BeautifulSoup(page.content, 'html.parser')
    for offer in bs.find_all('div', class_='offer-wrapper'):
        footer = offer.find('td', class_='bottom-cell')
        location = footer.find(
            'small', class_='breadcrumb').get_text().strip().split(',')[0]
        title = offer.find('strong').get_text().strip()
        price = parse_price(offer.find('p', class_='price').get_text().strip())
        cursor.execute('INSERT INTO offers VALUES (?, ?, ?)',
                       (title, price, location))
    db.commit()


db = sqlite3.connect('dane.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute(
        '''CREATE TABLE offers (name TEXT, price REAL, city TEXT)''')
    quit()


for page in range(1, 31):
    parse_page(page)

db.close
