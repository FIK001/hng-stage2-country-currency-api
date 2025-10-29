import os
from src.app import app
from src.db_connection import create_tables  # ✅ now correct

if __name__ == "__main__":
    create_tables()  # Ensure database tables exist
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
