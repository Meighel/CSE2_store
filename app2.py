#Can save data to a file (JSON)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def read_products_from_file():
    try:
        with open('products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  

def save_products_to_file(products):
    with open('products.json', 'w') as f:
        json.dump(products, f)

@app.route('/products', methods=['GET'])
def get_products():
    products = read_products_from_file()
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    products = read_products_from_file()
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not all(k in data for k in ('id', 'name', 'price')):
        return jsonify({'error': 'Missing product fields'}), 400
    products = read_products_from_file() 
    products.append(data)
    save_products_to_file(products) 
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = read_products_from_file()  
    products = [p for p in products if p['id'] != product_id]
    save_products_to_file(products)  
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
