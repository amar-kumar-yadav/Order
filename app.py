# LAst Modified By: Amar Kumar Yadav

from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Mongo DB connection
# Replace the mongodb connection string with yours
client = MongoClient('mongodb+srv://<username>:<password>@cluster0.pxhbxhe.mongodb.net/?retryWrites=true&w=majority')
db = client['Orders']

# Routes
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # input: This function expects a order id
    # output: Returns the order details for the specific order id
    order = db.Orders.find_one({'order_id': order_id})
    if order:
        return jsonify(order), 200
    else:
        return jsonify({'error': 'Order id not found'}), 404

@app.route('/average_products', methods=['GET'])
def get_average_products():
    # input: None
    # output: Returns the average product count
    total_orders = db.Orders.count_documents({})

    total_products = db.Orders.find()
    total_product_count = 0
    for order in total_products:
        total_product_count += order['product_count']

    average_products = total_product_count / total_orders

    return jsonify({'average_products': average_products}), 200


@app.route('/average_quantity/<int:product_id>', methods=['GET'])
def get_average_quantity(product_id):
    # input: This function expects a product id
    # output: Returns the average quantity in each order
    orders_with_product = db.Orders.find({'products.id': product_id})

    total_quantity = 0
    order_count = 0

    for order in orders_with_product:
        for product in order['products']:
            if product.get('id') == product_id:
                total_quantity += product.get('quantity', 0)
                order_count += 1

    average_quantity = total_quantity / order_count if order_count > 0 else 0

    return jsonify({'average_quantity': average_quantity}), 200

if __name__ == '__main__':
    app.run(debug=True)

