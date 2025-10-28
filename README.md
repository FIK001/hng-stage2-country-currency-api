````{"id":"83129","variant":"standard","title":"README.md File Content"}
# 🌍 Countries & Currency REST API

A **Flask-based REST API** that fetches, stores, and manages global country data (including flags, capitals, regions, populations, and currencies).  
Built for the **HNG Internship Stage 2 Backend Task**.

---

## 🚀 Features

- Fetches country data from the [REST Countries API](https://restcountries.com/v2/all)  
- Stores data in a **MySQL database**  
- Supports **CRUD operations** (GET, DELETE)  
- Includes **Swagger API documentation** via Flasgger  
- Filter and sort countries by **region, currency, or GDP**  
- `/refresh` endpoint to re-fetch country data from external APIs  
- `/status` endpoint to check database and refresh info  

---

## 🧠 Tech Stack

- Python 3.12+
- Flask
- Flasgger (Swagger UI)
- MySQL
- python-dotenv

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/hng-stage2.git
cd hng-stage2
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the project root with your database credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=countries_db
```

---

## 🗄️ Database Setup

Run these commands inside MySQL:
```sql
CREATE DATABASE countries_db;

USE countries_db;

CREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    capital VARCHAR(100),
    region VARCHAR(100),
    population BIGINT,
    flag VARCHAR(255),
    currency_name VARCHAR(100),
    currency_code VARCHAR(10),
    estimated_gdp FLOAT NULL
);
```

---

## 🏃 Run the Application

From your project root:
```bash
python -m src.app
```

You should see:
```
🌍 Fetching country data...
✅ Done! Inserted 250 countries. Failed: 0.
 * Running on http://127.0.0.1:5000
```

---

## 📘 API Documentation (Swagger)

Visit:
```
http://127.0.0.1:5000/docs
```

---

## 🧩 Sample Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/countries` | Get all countries (filter by region/currency) |
| GET | `/countries/<name>` | Get details of a specific country |
| DELETE | `/countries/<name>` | Delete a country by name |
| POST | `/refresh` | Refresh and update all countries |
| GET | `/status` | Check DB and refresh status |

---

## 🧑‍💻 Author
**Samuel Oluwafikunayomi**  
GitHub: [@FIK001](https://github.com/FIK001)  
Stack: Python / Flask  
Project: HNG Internship Stage 2

---

## 🏁 License
MIT License — free to use, modify, and distribute.
````
