import random
import requests
from bs4 import BeautifulSoup
import os
import sys
import json
import csv
from time import sleep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/106.0.0.0 Safari/537.36'
}

# Список под наши ссылки
fests_urls_list = []

# for i in range(0, 96, 24):
for i in range(0, 24, 24): # Тестируем на одном запросе
    # Вставляем ссылки динамически обновляющихся страниц inspect/network/fetch/payload
    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=15%20Oct%202022&to_date' +\
          f'=&maxprice=500&o={i}&bannertitle=May'

    # делаем запрос на страницы и получаем json данные
    req = requests.get(url, headers=headers)

    # Считываем полученные данные inspect/network/fetch/preview (нам нужен html)
    json_data = json.loads(req.text)

    # Получаем необходимый html
    html_response = json_data['html']

    # проверяем существует ли папка, и создаём её, если не существует
    directory = os.path.abspath(__file__)
    if not os.path.exists(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data'):
        os.makedirs(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data')

    # Сохраняем полученные данные в файл
    with open(f'data/index{i}.html', 'w') as file:
        file.write(html_response)

    # Открываем файл на чтение и считываем данные
    with open(f'data/index{i}.html') as file:
        src = file.read()

    # Передаём данные в BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')

    # Находим все ссылки на странице
    cards = soup.find_all('a', class_='card-details-link')

    # сохраняем ссылки в список
    for item in cards:
        fest_url = item.get('href')
        fests_urls_list.append(f'https://www.skiddle.com{fest_url}')

# print(fests_urls_list)

# Собираем информацию о фестивалях по собранным ссылкам
for url in fests_urls_list:
    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        # Забираем div с нужной информацией
        fest_name = soup.find('div', class_='MuiBox-root').find('h1').text
        print(fest_name)
        fest_info_block = soup.find('div', class_='css-1ik2gjq').find_all('div', class_='css-2re0kq')
        fest_date_all = fest_info_block[0].find_all('span')
        # fest_date_all = soup.find('div', class_='css-twt0ol').find_all('span')
        fest_date = fest_date_all[0].text + fest_date_all[1].text
        print(fest_date)
        fest_place = fest_info_block[1].find('span').text
        print(fest_place)
        min_price_al = fest_info_block[2].find_all('span')
        min_price = min_price_al[0].text + min_price_al[1].text
        print(min_price)
    except Exception as ex:
        print(ex)
        print('Some error')
