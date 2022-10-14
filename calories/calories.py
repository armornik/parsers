import random

import requests
from bs4 import BeautifulSoup
import os
import sys
import json
import csv
from time import sleep

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
#
# # Чтобы сайт не думал, что мы бот (inspect > Network > XHR обновить страницу и посмотреть запрос)
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/106.0.0.0 Safari/537.36'
}
#
# # Получаем страницу
# req = requests.get(url, headers=headers)
#
# # Получаем текст страницы
# src = req.text
#
directory = os.path.abspath(__file__)
#
# # Сохраняем страницу у себя, чтобы не беспокоить сайт
# with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}index.html', 'w', encoding='utf-8') as file:
#     file.write(src)


# # 2 ЭТАП
# # Дальше работаем с сохраненной страницей
# with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}index.html', encoding='utf-8') as file:
#     src = file.read()
#
# # Передаём данные в BeautifulSoup
# soup = BeautifulSoup(src, 'lxml')
#
# # Собираем все ссылки и сохраняем в словарь
# all_products_href = soup.find_all(class_='mzr-tc-group-item-href')
# all_categories_dict = {}
# for item in all_products_href:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_text] = item_href
#
# # Сохраняем в файл json
# with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}all_categories_dict.json', 'w', encoding='utf-8')\
#         as file:
#     # indent - отступ (чтобы не было в одну строку)
#     # ensure_ascii - для кодировки
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

# 3 этап работаем с json дальше
with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}all_categories_dict.json', encoding='utf-8')\
        as file:
    all_categories = json.load(file)
# Количество страниц с категориями
iteration_count = int(len(all_categories)) - 1
print(f'Всего итераций: {iteration_count}')
count = 0
# Заходим в категорию, собираем данные о химическом составе и записываем в файл
for category_name, category_href in all_categories.items():
    # Список символов, которые хотим заменить
    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    # Делаем запрос на страницы
    req = requests.get(url=category_href, headers=headers)

    # Сохраняем результат
    src = req.text
    # проверяем существует ли папка, и создаём её, если не существует
    if not os.path.exists(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data'):
        os.makedirs(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data')
    # Сохраняем страницы с именем категории
    with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data/{count}_{category_name}.html', 'w',
              encoding='utf-8') as file:
        file.write(src)

    with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data/{count}_{category_name}.html',
              encoding='utf-8') as file:
        src = file.read()
    # Передаём данные в BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')

    # Проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    # Собираем заголовки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    # print(table_head)
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    # Собираем данные в файл
    with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data/{count}_{category_name}.csv', 'w',
              encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # Собираем данные продуктов
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    # Для файла json
    product_info = []

    # Собираем данные о продуктах
    for item in products_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        # print(title)
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text
        # print(proteins)

        product_info.append(
            {
                'Title': title,
                'Calories': calories,
                'Proteins': proteins,
                'Fats': fats,
                'Carbohydrates': carbohydrates
            }
        )

        # Дозаписываем данные в файл
        with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data/{count}_{category_name}.csv', 'a',
                  encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data/{count}_{category_name}.json', 'w',
              encoding='utf-8') as file:
        # indent - отступ (чтобы не было в одну строку)
        # ensure_ascii - для кодировки
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итерация {count}. {category_name} записан...')
    iteration_count -= 1
    if iteration_count == 0:
        break
    print(f'Осталось итераций: {iteration_count}')

    sleep(random.randrange(2, 4))
