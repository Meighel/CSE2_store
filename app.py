#Saving only in memory

from flask import Flask, request, jsonify

app = Flask(__name__)
products = []

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not all(k in data for k in ('id', 'name', 'price')):
        return jsonify({'error': 'Missing product fields'}), 400
    products.append(data)
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
