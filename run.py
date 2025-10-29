import os
from src.app import app, create_tables

if __name__ == "__main__":
    # Ensure database tables exist before starting the app
    create_tables()
    
    # Get the port from environment variables (useful for PythonAnywhere or other hosts)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=port, debug=True)
