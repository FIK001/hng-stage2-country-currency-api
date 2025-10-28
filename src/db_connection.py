import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_connection():
    """
    Establish and return a MySQL database connection.
    Returns None if connection fails.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "countries_db"),
            raise_on_warnings=True
        )
        conn.autocommit = True  # Automatically commit transactions
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
