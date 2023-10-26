# URL = https://api.telegram.org/bot6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE/
# chat_id= 6325704944


import requests
import time

API_URL = 'http://api.telegram.org/bot'
BOT_TOKEN = '6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
GOAR_LIST = ['Малявка, это ты?)', 'А вот это?', 'Ну тут по-любому ты', 'Ладно, вот ты ахах']
ERROR_TEXT = 'Здесь должна быть картинка с котиком :('
TEXT = 'Опачки! Апдейтик'
MAX_COUNTER = 100

offset = -5
counter = 0
chat_id: int
cat_response: requests.Response
cat_url: str

requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={6325704944}&text={"Эй, напиши мне"}')

while counter < MAX_COUNTER:
    print('attempt =', counter)

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset+1}').json()   # берёт только последние 4 апдейта

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']

            cat_response = requests.get(API_CATS_URL)

            if cat_response.status_code == 200:
                cat_url = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_url}&caption={GOAR_LIST[counter%4]}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

            time.sleep(1)
            counter += 1