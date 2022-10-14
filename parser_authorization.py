import requests
from bs4 import BeautifulSoup as BS
from dotenv import dotenv_values
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    payload_env = dotenv_values(dotenv_path)


s = requests.Session()

# Пустой запрос на страницу
auth_html = s.get('https://smartprogress.do/')

# Отдаём результат в BS
auth_bs = BS(auth_html.content, 'html.parser')

# Получаем csrf_token
csrf = auth_bs.select('input[name=YII_CSRF_TOKEN]')[0]['value']

print(csrf)

# Создаём словарь с данными для входа на сайт (смотреть inspect > network > preverse log > all > login) после успешной
# авторизации
payload = {
    'YII_CSRF_TOKEN': csrf,
    'returnUrl': '/',
}

payload_end = {
    'UserLoginForm[rememberMe]': 1
}

payload = {**payload, **payload_env, **payload_end}

# Отправляем запрос через метод POST на страницу логина
answer = s.post('https://smartprogress.do/user/login/', data=payload)
answer_bs = BS(answer.content, 'html.parser')

print('Имя: {}\nУровень: {}\nОпыт: {}'.format(
    answer_bs.select('.user-menu__name')[0].text.strip(),
    answer_bs.select('.user-menu__info-text--lvl')[0].text.strip(),
    answer_bs.select('.user-menu__info-text--exp')[0].text.strip(),
))