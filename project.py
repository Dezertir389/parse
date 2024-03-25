from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)


class Search:
    def __init__(self, item):
        self.item = item

    def s_wb(self):
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={self.item}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                return response.text
        else:
            return None

    def s_av(self):
        url = f"https://www.avito.ru/kursk?q={self.item}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                return response.text
        else:
            return None


def find_best_deal(item):
    s = Search(item)
    wildberries_data = s.s_wb()
    avito_data = s.s_av()

    if wildberries_data and avito_data:
        best_deal = min(wildberries_data['price'], avito_data['price'])
        return {'best_deal': best_deal}
    else:
        error_message = 'Failed to fetch data from:'
        if not wildberries_data:
            error_message += ' Wildberries'
        if not avito_data:
            error_message += ' Avito'
        return {'error': error_message}


@app.route('/search', methods=['GET'])
def search():
    search_item = request.args.get('item')
    best_deal = find_best_deal(search_item)
    if 'error' in best_deal:
        return jsonify({'error': best_deal['error']}), 400
    else:
        return jsonify(best_deal)


if __name__ == '__main__':
    app.run(debug=True)