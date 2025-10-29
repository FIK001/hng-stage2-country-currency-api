from app import app
from src.db_connection import initialize_db
from pyngrok import ngrok
import os

initialize_db()
port = int(os.environ.get("PORT", 5000))
public_url = ngrok.connect(port)
print(f"Ngrok URL: {public_url}/docs/")

app.run(host="0.0.0.0", port=port, debug=False)
