from initialize_tables import initialize
from get_info import get_all_locations, get_all_products, get_all_purchases
from post_info import post_new_purchase, delete_purchase
from drop_info import drop_all
from flask import Flask, request, jsonify, render_template

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
    return render_template('index.html')

@app.route("/init", methods=['GET'])
def init():
    initialize()
    return "<p>Tables are initialized</p>", 200

@app.route("/get_products", methods=['GET'])
def get_products():
    result = get_all_products()
    return jsonify(result), 200

@app.route("/get_all_purchases", methods=['GET'])
def get_all_purchases_route():
    result = get_all_purchases()
    return jsonify(result), 200

@app.route("/post_purchase", methods=['POST'])
def post_purchase():
    data = request.get_json()
    id = post_new_purchase(
        data['payer'],
        data['shop'],
        data['location'],
        data['date'],
        [(el['name'], el['price'], el['amount'], el['flag']) for el in data['products']]
    )
    return jsonify({'purchase_id': id}), 200

@app.route("/delete_purchase/<int:purchase_id>", methods=['DELETE'])
def delete_purchase_route(purchase_id):
    deleted = delete_purchase(purchase_id)
    if deleted is None:
        return jsonify({'error': 'Не получилось удалить покупку'}), 400
    return jsonify({'purchase_id': purchase_id, 'deleted': True}), 200

@app.route("/post_drop_all", methods=['POST'])
def post_drop():
    drop_all()
    return '<p>Успешно удалили все базы</p>'

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()