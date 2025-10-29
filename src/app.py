import os
from flask import Flask, jsonify, request, send_file
from flasgger import Swagger
from src.db_connection import get_connection
from src.fetch_countries import (
    get_countries,
    get_country_by_name,
    delete_country_by_name,
    get_status,
    fetch_and_store_countries  # replaces old refresh_countries
)
from src.image_generator import generate_summary_image  # optional

# -----------------------------
# APP INITIALIZATION
# -----------------------------
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
# ROOT ROUTE
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🌍 Countries API is running successfully!",
        "docs": "Visit /docs for Swagger UI",
        "endpoints": {
            "/countries": "Get all countries (with optional filters)",
            "/countries/<name>": "Get or delete a specific country",
            "/refresh": "Fetch and refresh countries from external APIs",
            "/status": "Check database and refresh status",
            "/countries/image": "Get summary image of countries (optional)"
        }
    }), 200

# -----------------------------
# GET ALL COUNTRIES
# -----------------------------
@app.route("/countries", methods=["GET"])
def list_countries():
    region = request.args.get("region")
    currency = request.args.get("currency")
    sort = request.args.get("sort")
    data = get_countries(region, currency, sort)
    return jsonify(data), 200

# -----------------------------
# GET / DELETE COUNTRY BY NAME
# -----------------------------
@app.route("/countries/<name>", methods=["GET", "DELETE"])
def country_by_name(name):
    if request.method == "GET":
        country = get_country_by_name(name)
        if country:
            return jsonify(country), 200
        return jsonify({"error": "Country not found"}), 404
    else:  # DELETE
        deleted = delete_country_by_name(name)
        if deleted:
            return jsonify({"message": f"{name} deleted successfully!"}), 200
        return jsonify({"error": "Country not found or already deleted"}), 404

# -----------------------------
# REFRESH COUNTRIES
# -----------------------------
@app.route("/countries/refresh", methods=["POST"])
def refresh_data():
    try:
        fetch_and_store_countries()
        try:
            generate_summary_image()
        except Exception:
            print("⚠️ Summary image generation skipped or failed.")
        return jsonify({"message": "Countries refreshed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# SUMMARY IMAGE ENDPOINT
# -----------------------------
@app.route("/countries/image", methods=["GET"])
def country_image():
    image_path = "cache/summary.png"
    if not os.path.exists(image_path):
        return jsonify({"error": "Summary image not found"}), 404
    return send_file(image_path, mimetype="image/png")

# -----------------------------
# STATUS ENDPOINT
# -----------------------------
@app.route("/status", methods=["GET"])
def status():
    return jsonify(get_status()), 200
