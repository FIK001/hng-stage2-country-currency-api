from src.db_connection import get_connection

def fetch_and_store_countries():
    import requests
    conn = get_connection()
    cursor = conn.cursor()

    url = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to fetch data")
        return False

    cursor.execute("DELETE FROM countries")  # Clear old data

    success = 0
    fail = 0

    for country in data:
        try:
            name = country.get("name")
            capital = country.get("capital")
            region = country.get("region")
            population = country.get("population")
            flag = country.get("flag")
            currency = country.get("currencies")[0] if country.get("currencies") else {}
            currency_name = currency.get("name")
            currency_code = currency.get("code")
            estimated_gdp = None

            cursor.execute("""
                INSERT INTO countries (name, capital, region, population, flag, currency_name, currency_code, estimated_gdp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, capital, region, population, flag, currency_name, currency_code, estimated_gdp))

            success += 1
        except Exception as e:
            fail += 1
            print(f"❌ Error inserting {country.get('name')}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n✅ Done! Inserted {success} countries. Failed: {fail}.")
    return True


# -----------------------------
# Utility Functions for API
# -----------------------------
def get_countries(region=None, currency=None, sort=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM countries WHERE 1=1"
    params = []

    if region:
        query += " AND region = %s"
        params.append(region)
    if currency:
        query += " AND currency_code = %s"
        params.append(currency)
    if sort == "gdp_asc":
        query += " ORDER BY estimated_gdp ASC"
    elif sort == "gdp_desc":
        query += " ORDER BY estimated_gdp DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_country_by_name(name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM countries WHERE name = %s", (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def delete_country_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM countries WHERE name = %s", (name,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted


def get_status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM countries")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_countries": total, "status": "active"}
