from datetime import datetime, timezone
import json


def create_tables(cursor, connection):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        user_id INTEGER NOT NULL,
        weather TEXT,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    connection.commit()


def get_user_by_id(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


def post_city_data(cursor, connection, request, weather_info):
    cursor.execute(
        "INSERT INTO cities (name, latitude, longitude, user_id, weather, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (request.name,
         request.latitude,
         request.longitude,
         request.user_id,
         json.dumps(weather_info),
         datetime.now(timezone.utc).isoformat())
    )
    connection.commit()


def get_cities(cursor, user_id):
    cursor.execute("SELECT name, latitude, longitude FROM cities WHERE user_id = ?", (user_id,))
    cities = cursor.fetchall()
    return cities


def get_city_by_name_and_user(cursor, city_name, user_id):
    cursor.execute("SELECT * FROM cities WHERE name = ? AND user_id = ?", (city_name, user_id))
    return cursor.fetchone()
