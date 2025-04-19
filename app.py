from flask import Flask, request, jsonify

app = Flask(__name__)

# Product to Center and Weight Map
product_info = {
    'A': {'center': 'C1', 'weight': 3},
    'B': {'center': 'C1', 'weight': 2},
    'C': {'center': 'C1', 'weight': 8},
    'D': {'center': 'C2', 'weight': 12},
    'E': {'center': 'C2', 'weight': 25},
    'F': {'center': 'C2', 'weight': 15},
    'G': {'center': 'C3', 'weight': 0.5},
    'H': {'center': 'C3', 'weight': 1},
    'I': {'center': 'C3', 'weight': 2}
}

# Delivery Cost Matrix (One-way)
costs = {
    'C1': {'L1': 10, 'C2': 20, 'C3': 30},
    'C2': {'L1': 15, 'C1': 20, 'C3': 25},
    'C3': {'L1': 20, 'C1': 30, 'C2': 25}
}

def calculate_total_cost(order):
    center_weight_map = {'C1': 0, 'C2': 0, 'C3': 0}

    for product, qty in order.items():
        if product not in product_info:
            continue
        product_data = product_info[product]
        center = product_data['center']
        weight = product_data['weight']
        center_weight_map[center] += weight * qty

    total_cost = 0
    for center, total_weight in center_weight_map.items():
        if total_weight > 0:
            trips = 1  # assuming single delivery per center for now
            total_cost += trips * costs[center]['L1']

    return total_cost

@app.route('/calculate', methods=['POST'])
def calculate():
    order = request.get_json()
    if not order:
        return jsonify({"error": "Invalid input"}), 400
    total_cost = calculate_total_cost(order)
    return jsonify({"total_cost": total_cost})

if __name__ == '_main_':
    app.run(debug=True)
