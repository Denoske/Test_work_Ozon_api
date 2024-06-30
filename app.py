import os
import requests
import logging
import json
from flask import Flask, request, jsonify
import threading
logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
class OzonAPI:
    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key
        
    def get_actions(self):
        url = "https://api-seller.ozon.ru/v1/actions"
        headers = {
            "Content-Type": "application/json",
            "Client-Id": self.client_id,
            "Api-Key": self.api_key
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_action_candidates(self, action_id,limit,offset):
        url = 'https://api-seller.ozon.ru/v1/actions/candidates'
        headers = {
            'Content-Type': 'application/json',
            'Client-Id': self.client_id,
            'Api-Key': self.api_key
        }
        payload = {
            'action_id': action_id,
            'limit': limit,
            'offset': offset,
        }
        response = requests.post(url, headers=headers, json=payload).json()
        return response
        
    def add_products_to_action(self,action_id, max_action_price,product_id,stock):
        url = 'https://api-seller.ozon.ru/v1/actions/products/activate'
        headers = {
            'Content-Type': 'application/json',
            'Client-Id': self.client_id,
            'Api-Key': self.api_key
        }
        payload = {
            'action_id' : action_id,
            'products': [{
                'max_action_price': max_action_price,
                'product_id': product_id,
                'stock': stock
            }]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

ozon_api = OzonAPI('XXX', 'XXX')

@app.route('/get_actions', methods=['GET'])
def get_actions():
    actions = ozon_api.get_actions()
    return jsonify(actions)

@app.route('/get_action_candidates', methods=['GET'])
def get_action_candidates():
    action_candidates = ozon_api.get_action_candidates(1139903,10,0)
    return jsonify(action_candidates)

@app.route('/add_products_to_action', methods=['GET'])
def add_products_to_action():
    action_id = 1139903
    data = ozon_api.get_action_candidates(action_id,10,0)
    filtered_products = [product for product in data['result']['products'] if ((product['price'] - product['max_action_price']) / product['price']) < 0.1]
    if filtered_products:
        for product in filtered_products:
            result = ozon_api.add_products_to_action(action_id,product['max_action_price'], product['id'], product['stock'])
            return jsonify(result)
    else:
        return jsonify({'message': 'No products found'})

if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '127.0.0.1','port':5000}).start()
