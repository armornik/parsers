import requests
from bs4 import BeautifulSoup
import os
import sys
import json
from time import sleep
import random
import traceback

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/106.0.0.0 Safari/537.36'
}

# # Часть 1 скачиваем необходимые страницы себе
# for i in range(0, 741, 20):
#     # Вставляем ссылки динамически обновляющихся страниц inspect/network/XHR
#     url = f'https://www.bundestag.de/ajax/filterlist/de/abgeordnete/biografien/862712-862712?limit=' \
#           f'20&noFilterSet=true&offset={i}'
#
#     # делаем запрос на страницы и получаем json данные
#     req = requests.get(url, headers=headers)
#
#     # Забираем контент
#     result = req.content
#
#     # проверяем существует ли папка, и создаём её, если не существует
#     directory = os.path.abspath(__file__)
#     if not os.path.exists(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data'):
#         os.makedirs(f'{directory.replace(os.path.basename(sys.argv[0]), "")}data')
#
#     # Сохраняем полученные данные в файл
#     with open(f'data/index{i}.html', 'w') as file:
#         file.write(str(result))


# # 2 Работаем со скачанными файлами
# persons_url_list = []
#
# for i in range(0, 741, 20):
#     # Открываем файл на чтение и считываем данные
#     with open(f'data/index{i}.html') as file:
#         src = file.read()
#
#     # Передаём данные в BeautifulSoup
#     soup = BeautifulSoup(src, 'lxml')
#
#     # Получаем ссылки на карточки со страницы
#
#     # Получаем классы в которых содержатся ссылки и сами ссылки
#     persons = [persons_url_list.append(div.a['href']) for div in soup.find_all('div', class_="bt-slide-content")]
#
# # Сохраняемые данные в файл
# with open('person_url_list.txt', 'a') as file:
#     for person_url in persons_url_list:
#         file.write(f'{person_url}\n')


# 3
# Считываем полученные данные в новый список
with open('person_url_list.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]
    # print(lines)

    # Словарь для окончательных данных
    data_dict = []
    count = 0
    for line in lines:
        q = requests.get(f'https://www.bundestag.de{line}')

        # Получаем содержимое страниц
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        try:
            # Получаем имя и партию
            person = soup.find(class_='bt-biografie-name').find('h3').text

            # Разделяем имя и партию
            person_name, person_company = person.strip().split(',')

            # Получаем ссылки на сети
            social_networks = soup.find_all(class_='bt-link-extern')
            social_networks_urls = []
            for item in social_networks:
                social_networks_urls.append(item.get('href'))
            # print(social_networks_urls)

            data = {
                'person_name': person_name,
                'company_name': person_company.strip(),
                'social_networks_urls': social_networks_urls
            }

            data_dict.append(data)
            sleep(random.randrange(2, 4))

            with open('data.json', 'w') as json_file:
                json.dump(data_dict, json_file, indent=4)

            count += 1
            print(f'# Итерация {count} записан...')

        except Exception as E:
            print(E)
            print(traceback.format_exc())
