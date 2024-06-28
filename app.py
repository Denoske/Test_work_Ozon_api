import requests
from flask import Flask, request, jsonify, make_response
import threading

app = Flask(__name__)

class OzonAPI:
    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key

    def get_products(self):
        url = 'https://api-seller.ozon.ru/v2/product'
        headers = {
            'Client-Id': self.client_id,
            'Api-Key': self.api_key
        }
        response = requests.get(url, headers=headers)
        return response
    def get_actions(self):
        url = 'https://api-seller.ozon.ru/v1/actions'
        headers = {
            'Client-Id': self.client_id,
            'Api-Key': self.api_key
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_action_candidates(self):
        url = 'https://api-seller.ozon.ru/v1/actions/candidates'
        headers = {
            'Client-Id': self.client_id,
            'Api-Key': self.api_key
        }
        response = requests.get(url, headers=headers)
        return response

#ozon_api = OzonAPI('###', '###')
ozon_api = OzonAPI('0', '0')

@app.route('/get_actions', methods=['GET']) # Посмотреть все акции
def get_actions():
    actions = ozon_api.get_actions()
    return jsonify(actions)

@app.route('/get_action_candidates', methods=['GET']) # Получить товары доступные для акции
def get_action_candidates():
    action_candidates = ozon_api.get_action_candidates()
    return list(action_candidates)

@app.route('/products', methods=['GET']) # Получить список товаров
def get_products():
    products = ozon_api.get_products()
    return list(products)

if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '127.0.0.1','port':5000}).start()
