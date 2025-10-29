from flask import Flask, jsonify, request
from flasgger import Swagger
from src.db_connection import get_connection
from src.fetch_countries import (
    get_countries,
    get_country_by_name,
    delete_country_by_name,
    get_status,
    fetch_and_store_countries
)

app = Flask(__name__)

# -----------------------------
# Swagger Configuration
# -----------------------------
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
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
@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint
    ---
    tags:
      - Home
    responses:
      200:
        description: Welcome message and API endpoints
    """
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
# Get All Countries
# -----------------------------
@app.route("/countries", methods=["GET"])
def list_countries():
    """
    Get all countries
    ---
    tags:
      - Countries
    parameters:
      - name: region
        in: query
        type: string
        required: false
        description: Filter by region
      - name: currency
        in: query
        type: string
        required: false
        description: Filter by currency
      - name: sort
        in: query
        type: string
        required: false
        description: Sort field (name, population)
    responses:
      200:
        description: List of countries
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              capital:
                type: string
              region:
                type: string
    """
    region = request.args.get("region")
    currency = request.args.get("currency")
    sort = request.args.get("sort")
    data = get_countries(region, currency, sort)
    return jsonify(data), 200

# -----------------------------
# Get Country by Name
# -----------------------------
@app.route("/countries/<name>", methods=["GET"])
def get_country(name):
    """
    Get a specific country by name
    ---
    tags:
      - Countries
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Country name
    responses:
      200:
        description: Country found
        schema:
          type: object
          properties:
            name:
              type: string
            capital:
              type: string
            region:
              type: string
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
@app.route("/countries/<name>", methods=["DELETE"])
def delete_country(name):
    """
    Delete a country by name
    ---
    tags:
      - Countries
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Country name
    responses:
      200:
        description: Country deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Country not found or already deleted
    """
    deleted = delete_country_by_name(name)
    if deleted:
        return jsonify({"message": f"{name} deleted successfully!"}), 200
    return jsonify({"error": "Country not found or already deleted"}), 404

# -----------------------------
# Refresh Countries
# -----------------------------
@app.route("/refresh", methods=["POST"])
def refresh_data():
    """
    Refresh countries from external APIs
    ---
    tags:
      - Admin
    responses:
      200:
        description: Countries refreshed successfully
      500:
        description: Error occurred during refresh
    """
    try:
        fetch_and_store_countries()
        return jsonify({"message": "Countries refreshed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Status
# -----------------------------
@app.route("/status", methods=["GET"])
def status():
    """
    Get database and refresh status
    ---
    tags:
      - Admin
    responses:
      200:
        description: Status information
        schema:
          type: object
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
