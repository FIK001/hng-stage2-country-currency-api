import os
from flask import Flask, jsonify, request, send_file
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
from src.db_connection import get_connection
from src.fetch_countries import (
    fetch_and_store_countries,
    get_countries,
    get_country_by_name,
    delete_country_by_name,
    get_status
)
from src.image_generator import generate_summary_image  # optional

# Load environment variables
load_dotenv()

# -----------------------------
# APP INITIALIZATION
# -----------------------------
app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Countries API",
    description="RESTful API for fetching, refreshing, and managing countries data.",
    doc="/docs"
)

# -----------------------------
# API NAMESPACE
# -----------------------------
ns = api.namespace("countries", description="Country operations")

# -----------------------------
# MODEL SCHEMA (Swagger docs)
# -----------------------------
country_model = api.model("Country", {
    "name": fields.String(required=True, description="Country name"),
    "capital": fields.String(description="Capital city"),
    "region": fields.String(description="Region"),
    "population": fields.Integer(description="Population"),
    "currency_code": fields.String(description="Currency code"),
    "exchange_rate": fields.Float(description="Exchange rate (relative to USD)"),
    "estimated_gdp": fields.Float(description="Estimated GDP"),
    "flag_url": fields.String(description="Flag image URL"),
    "last_refreshed_at": fields.String(description="Timestamp of last refresh")
})

# -----------------------------
# ROUTES
# -----------------------------
@ns.route("/")
class AllCountries(Resource):
    @ns.marshal_list_with(country_model)
    def get(self):
        """Retrieve all countries (supports filtering and sorting)"""
        region = request.args.get("region")
        currency = request.args.get("currency")
        sort = request.args.get("sort")
        return get_countries(region=region, currency=currency, sort=sort)

@ns.route("/<string:name>")
class CountryByName(Resource):
    @ns.marshal_with(country_model)
    def get(self, name):
        country = get_country_by_name(name)
        if not country:
            return {"error": "Country not found"}, 404
        return country

    def delete(self, name):
        success = delete_country_by_name(name)
        if not success:
            return {"error": "Country not found"}, 404
        return {"message": f"{name} deleted successfully"}, 200

@ns.route("/refresh")
class RefreshCountries(Resource):
    def post(self):
        """Fetch and refresh all country + exchange rate data"""
        try:
            fetch_and_store_countries()
            try:
                generate_summary_image()
            except Exception:
                print("⚠️ Summary image generation skipped or failed.")
            return {"message": "Countries refreshed successfully"}, 200
        except Exception as e:
            return {"error": "Internal server error", "details": str(e)}, 500

@ns.route("/image")
class CountryImage(Resource):
    def get(self):
        """Serve the summary image"""
        image_path = "cache/summary.png"
        if not os.path.exists(image_path):
            return {"error": "Summary image not found"}, 404
        return send_file(image_path, mimetype="image/png")

# -----------------------------
# STATUS ENDPOINT
# -----------------------------
@app.route("/status")
def status():
    return jsonify(get_status())

# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Countries API!",
        "docs": "/docs",
        "example_endpoints": {
            "all_countries": "/countries/",
            "country_by_name": "/countries/Nigeria",
            "refresh_data": "/countries/refresh",
            "status": "/status"
        }
    })

# -----------------------------
# Helper function to create tables
# -----------------------------
def create_tables():
    from src.db_connection import initialize_db
    initialize_db()
