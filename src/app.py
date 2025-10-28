from flask import Flask, jsonify, request
from flasgger import Swagger
from src.db_connection import get_connection
from src.fetch_countries import get_countries, get_country_by_name, delete_country_by_name, get_status
from src.fetch_countries import fetch_and_store_countries  # ✅ this replaces refresh_countries

app = Flask(__name__)

# -----------------------------
# Swagger Configuration
# -----------------------------
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "info": {
        "title": "🌍 Countries API",
        "description": "API for managing and querying country data fetched from RESTCountries and exchange rate APIs.",
        "version": "1.0",
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


# -----------------------------
# Root Route
# -----------------------------
@app.route('/')
def home():
    return jsonify({
        "message": "🌍 Countries API is running successfully!",
        "docs": "Visit /docs for Swagger UI",
        "endpoints": {
            "/countries": "Get all countries (with optional filters)",
            "/countries/<name>": "Get or delete a specific country",
            "/refresh": "Fetch and refresh countries from external APIs",
            "/status": "Check database and refresh status"
        }
    }), 200


# -----------------------------
# Get All Countries (with filters & sort)
# -----------------------------
@app.route('/countries', methods=['GET'])
def list_countries():
    """
    Get all countries (with filters and sorting)
    ---
    parameters:
      - name: region
        in: query
        type: string
        required: false
        description: Filter by region (e.g. Africa, Europe)
      - name: currency
        in: query
        type: string
        required: false
        description: Filter by currency code (e.g. USD, NGN)
      - name: sort
        in: query
        type: string
        required: false
        description: Sort by GDP (gdp_asc or gdp_desc)
    responses:
      200:
        description: List of countries
    """
    region = request.args.get('region')
    currency = request.args.get('currency')
    sort = request.args.get('sort')

    data = get_countries(region, currency, sort)
    return jsonify(data), 200


# -----------------------------
# Get Country by Name
# -----------------------------
@app.route('/countries/<name>', methods=['GET'])
def get_country(name):
    """
    Get a specific country by name
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Country name
    responses:
      200:
        description: Country details
      404:
        description: Country not found
    """
    country = get_country_by_name(name)
    if country:
        return jsonify(country), 200
    return jsonify({"error": "Country not found"}), 404


# -----------------------------
# Delete Country by Name
# -----------------------------
@app.route('/countries/<name>', methods=['DELETE'])
def delete_country(name):
    """
    Delete a specific country by name
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Country name to delete
    responses:
      200:
        description: Deletion successful
      404:
        description: Country not found
    """
    deleted = delete_country_by_name(name)
    if deleted:
        return jsonify({"message": f"{name} deleted successfully!"}), 200
    return jsonify({"error": "Country not found or already deleted"}), 404


# -----------------------------
# Refresh Countries (re-fetch external data)
# -----------------------------
@app.route('/refresh', methods=['POST'])
def refresh_data():
    """
    Refresh countries data from external APIs
    ---
    responses:
      200:
        description: Countries refreshed successfully
      500:
        description: Failed to refresh data
    """
    try:
        fetch_and_store_countries()
        return jsonify({"message": "Countries refreshed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Status
# -----------------------------
@app.route('/status', methods=['GET'])
def status():
    """
    Get database status and last refresh time
    ---
    responses:
      200:
        description: Returns total countries and last refresh timestamp
    """
    info = get_status()
    return jsonify(info), 200


# -----------------------------
# Run Server
# -----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
