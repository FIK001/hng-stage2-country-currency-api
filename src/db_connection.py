import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "countries_db"),
            raise_on_warnings=True
        )
        conn.autocommit = True
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None


def create_tables():
    """
    Create the 'countries' table if it does not exist
    """
    conn = get_connection()
    if not conn:
        print("❌ Cannot create tables because database connection failed.")
        return

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name VARCHAR(100) PRIMARY KEY,
            capital VARCHAR(100),
            region VARCHAR(50),
            population BIGINT,
            currency_code VARCHAR(10),
            exchange_rate FLOAT,
            estimated_gdp FLOAT,
            flag_url VARCHAR(255),
            last_refreshed_at DATETIME
        )
    """)
    cursor.close()
    conn.close()
    print("✅ Database tables ensured.")
