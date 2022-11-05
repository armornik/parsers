# Firefox driver:
# https://chromedriver.storage.googleapis.com/index.html
#
# Chrome driver:
# https://github.com/mozilla/geckodriver/releases
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os


def get_data(url: str):
    # inspect -> network -> all -> most_luxe.php -> Request Headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'user - agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36'
    }

    req = requests.get(url, headers=headers)
    # print(req.encoding)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    # get hotels urls
    r = requests.get('https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most', headers=headers)
    # Передаём данные в BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')

    hotels_cards = soup.find_all('div', class_='hotel_card_dv')
    for hotel_url in hotels_cards:
        hotel_url = hotel_url.find('a').get('href')
        print(hotel_url)


def get_data_with_selenium(url: str):
    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36')

    # try:
    #     directory = os.path.abspath(__file__)
    #     driver = webdriver.Firefox(
    #         executable_path=f'{directory}\geckodriver.exe',
    #         options=options
    #     )
    #     driver.get(url=url)
    #     time.sleep(5)
    #
    #     with open('index_selenum.html', 'w', encoding='utf-8') as file:
    #         file.write(driver.page_source)
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     driver.close()
    #     driver.quit()

    with open('index_selenum.html', 'r', encoding='utf-8') as file:
        src = file.read()

    # get hotels urls
    soup = BeautifulSoup(src, 'lxml')

    hotels_cards = soup.find_all('div', class_='hotel_card_dv')
    for hotel_url in hotels_cards:
        hotel_url = 'https://tury.ru/' + hotel_url.find('a').get('href')
        print(hotel_url)


def main():
    # get_data('https://tury.ru/hotel/most_luxe.php')
    get_data_with_selenium('https://tury.ru/hotel/most_luxe.php')


if __name__ == '__main__':
    main()
