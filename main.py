from initialize_tables import initialize
from get_info import get_all_locations, get_all_products
from post_info import post_new_purchase
from drop_info import drop_all
from flask import Flask, request, jsonify

def testing():
    initialize()
    print(get_all_locations())
    post_new_purchase('Misha', 'Пятерочка', 'Подрезково', '11/08/2026', [('Молоко', 76, 1, 'common')])
    post_new_purchase('Masha', 'Магнит', 'Химки', '12/08/2026', [('Хлеб', 45, 1, 'mine')])
    print(get_all_products())
    drop_all()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to Common Budget!</p>" \
    "<p>Enter /get_products to get JSON with all products</p>" \
    "<p>Enter /post_purchase with JSON to post new purhase</p>"

@app.route("/init", methods=['GET'])
def init():
    initialize()
    return "<p>Tables are initialized</p>", 200

@app.route("/get_products", methods=['GET'])
def get_products():
    result = get_all_products()
    return jsonify(result), 200

@app.route("/post_purchase", methods=['POST'])
def post_purchase():
    data = request.get_json()
    id = post_new_purchase(data['payer'], data['shop'], data['location'], data['date'], 
                           [(el['name'], el['price'], el['amount'], el['flag']) for el in data['products']])
    return jsonify({'purchase_id' : id}), 200

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()