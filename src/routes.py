import os
from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Resource, fields, Namespace
from src.app import create_tables, refresh_countries, get_countries, get_status
from src.image_generator import generate_summary_image  # optional

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Countries API",
    description="API for fetching countries",
    doc="/docs"  # Swagger UI available here
)

# -----------------------------
# Namespace
# -----------------------------
ns = api.namespace("countries", description="Country operations")

# -----------------------------
# Models
# -----------------------------
country_model = api.model("Country", {
    "name": fields.String(required=True, description="Country name"),
    "capital": fields.String(description="Capital city"),
    "region": fields.String(description="Region"),
    "population": fields.Integer(description="Population"),
    "currency_code": fields.String(description="Currency code"),
    "exchange_rate": fields.Float(description="Exchange rate"),
    "estimated_gdp": fields.Float(description="Estimated GDP"),
    "flag_url": fields.String(description="Flag URL"),
    "last_refreshed_at": fields.String(description="Last refreshed timestamp")
})

status_model = api.model("Status", {
    "total_countries": fields.Integer(description="Total number of countries"),
    "last_refreshed_at": fields.String(description="Last refresh timestamp")
})

# -----------------------------
# Routes / Resources
# -----------------------------
@ns.route("/")
class AllCountries(Resource):
    @ns.marshal_list_with(country_model)
    @ns.doc(params={"region": "Filter by region", "currency": "Filter by currency code", "sort": "Sort by GDP: gdp_desc or gdp_asc"})
    def get(self):
        """Get all countries with optional filters and sorting"""
        region = request.args.get("region")
        currency = request.args.get("currency")
        sort = request.args.get("sort")
        return get_countries(region=region, currency=currency, sort=sort)

@ns.route("/<string:name>")
class CountryByName(Resource):
    @ns.marshal_with(country_model)
    def get(self, name):
        """Get a single country by name"""
        country = next((c for c in get_countries() if c["name"].lower() == name.lower()), None)
        if not country:
            api.abort(404, f"Country '{name}' not found")
        return country

    def delete(self, name):
        """Delete a country by name"""
        from src.app import delete_country_by_name
        success = delete_country_by_name(name)
        if not success:
            api.abort(404, f"Country '{name}' not found")
        return {"message": f"{name} deleted successfully"}, 200

@ns.route("/refresh")
class RefreshCountries(Resource):
    def post(self):
        """Refresh all countries and exchange rates"""
        success = refresh_countries()
        if not success:
            api.abort(503, "External data source unavailable")
        # Generate summary image
        generate_summary_image()
        return {"message": "Countries refreshed successfully"}, 200

@ns.route("/image")
class CountryImage(Resource):
    def get(self):
        """Serve summary image"""
        image_path = "cache/summary.png"
        if not os.path.exists(image_path):
            api.abort(404, "Summary image not found")
        return send_file(image_path, mimetype="image/png")

# -----------------------------
# Status endpoint
# -----------------------------
@api.route("/status")
class Status(Resource):
    @api.marshal_with(status_model)
    def get(self):
        """Get status of database"""
        return get_status()

# -----------------------------
# Home route
# -----------------------------
@app.route("/")
def home():
    return "Welcome to the Countries API! Visit /docs for API documentation."

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    create_tables()
    refresh_countries()  # optional on startup
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
