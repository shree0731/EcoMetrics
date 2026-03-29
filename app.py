from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_sustainability, train_model, load_model
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Pre-load model on startup
print("Loading ML model...")
try:
    load_model()
    print("Model ready!")
except Exception as e:
    print(f"Model load failed, will train on first request: {e}")


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "EcoMetrics API is running"})


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        energy = data.get('energy')
        water = data.get('water')
        co2 = data.get('co2')

        # Validate inputs
        if energy is None or water is None or co2 is None:
            return jsonify({"error": "Missing required fields: energy, water, co2"}), 400

        try:
            energy = float(energy)
            water = float(water)
            co2 = float(co2)
        except (ValueError, TypeError):
            return jsonify({"error": "All inputs must be numeric values"}), 400

        if energy < 0 or water < 0 or co2 < 0:
            return jsonify({"error": "All inputs must be non-negative values"}), 400

        result = predict_sustainability(energy, water, co2)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route('/products', methods=['GET'])
def get_products():
    """Return all product environmental data."""
    products = {
        "energy_consumption": [
            {"product": "Laptop", "value": 350, "unit": "MJ"},
            {"product": "Smartphone", "value": 200, "unit": "MJ"},
            {"product": "Steel Water Bottle", "value": 60, "unit": "MJ"},
            {"product": "Cloth Shopping Bag", "value": 20, "unit": "MJ"},
            {"product": "Glass Bottle", "value": 12, "unit": "MJ"},
            {"product": "LED Bulb", "value": 15, "unit": "MJ"},
            {"product": "Plastic Shopping Bag", "value": 6, "unit": "MJ"},
            {"product": "Chips Packet", "value": 5, "unit": "MJ"},
            {"product": "Milk Packet", "value": 4, "unit": "MJ"},
            {"product": "Paper Notebook", "value": 6, "unit": "MJ"},
            {"product": "Aluminum Can", "value": 10, "unit": "MJ"}
        ],
        "co2_emissions": [
            {"product": "Laptop", "value": 200, "unit": "kg"},
            {"product": "Smartphone", "value": 70, "unit": "kg"},
            {"product": "Steel Water Bottle", "value": 8, "unit": "kg"},
            {"product": "Cotton T-Shirt", "value": 5, "unit": "kg"},
            {"product": "LED Bulb", "value": 3, "unit": "kg"},
            {"product": "Glass Jar", "value": 1.4, "unit": "kg"},
            {"product": "Aluminum Can", "value": 1.5, "unit": "kg"},
            {"product": "Paper Notebook", "value": 1, "unit": "kg"},
            {"product": "Chips Packet", "value": 0.5, "unit": "kg"}
        ],
        "water_consumption": [
            {"product": "Cotton T-Shirt", "value": 2700, "unit": "L"},
            {"product": "Laptop", "value": 1500, "unit": "L"},
            {"product": "Smartphone", "value": 900, "unit": "L"},
            {"product": "Cloth Shopping Bag", "value": 100, "unit": "L"},
            {"product": "Paper Notebook", "value": 50, "unit": "L"},
            {"product": "Steel Water Bottle", "value": 40, "unit": "L"},
            {"product": "Cardboard Box", "value": 30, "unit": "L"},
            {"product": "LED Bulb", "value": 10, "unit": "L"},
            {"product": "Glass Bottle", "value": 6, "unit": "L"}
        ]
    }
    return jsonify(products), 200


if __name__ == '__main__':
    # Train model if not exists
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    if not os.path.exists(model_path):
        print("Training model for first time...")
        train_model()

    app.run(debug=True, host='0.0.0.0', port=5000)
