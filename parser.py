import requests
from bs4 import BeautifulSoup as BS

page = 1

anchor = True

while anchor:
    # Получаем данные со страницы
    result_page = requests.get(f'https://stopgame.ru/review/p{page}?subsection=izumitelno')

    # Отдаём результат в BS
    html_page = BS(result_page.content, 'html.parser')

    # Выбираем все статьи
    items = html_page.select('._default-grid_1fhuj_203')

    # Перебираем наши селекторы
    if len(items):
        for el in items:
            if len(el) == 35:
                title = el.select('._card__bottom_1akif_1 > ._card__content_1akif_357 > a')
                # Выводим название каждой игры с 1-ой страницы
                for game in title:
                    print(game.text)
                page += 1
                print(page)
            else:
                print(len(el))
                print(len(el))
                print(len(el))

                title = el.select('._card__bottom_1akif_1 > ._card__content_1akif_357 > a')
                # Выводим название каждой игры с 1-ой страницы
                for game in title:
                    print(game.text)
                anchor = False
                break
    else:
        break

# # Получаем данные со страницы
# result_page = requests.get('https://stopgame.ru/review/p1?subsection=izumitelno')
#
# # Отдаём результат в BS
# html_page = BS(result_page.content, 'html.parser')
#
# # Перебираем наши селекторы
# for el in html_page.select('._default-grid_1fhuj_203'):
#     # title = el.select('._card__title_1akif_1 _card__title--has-subtitle_1akif_1 > a')
#     title = el.select('._card__bottom_1akif_1 > ._card__content_1akif_357 > a')
#     # print(title)
#     # Выводим название каждой игры с 1-ой страницы
#     for game in title:
#         print(game.text)
