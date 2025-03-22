import json
import sqlite3
import time
from datetime import datetime, timezone, date
from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
import aiohttp
from request_models import WeatherRequest, OPEN_METEO_URL, CityMonitorRequest, RegisterUserRequest, TimeWeatherRequest
from db import create_tables, get_user_by_id, post_city_data, get_cities, get_city_by_name_and_user

app = FastAPI()

db_path = "weather.db"
# подключение к БД
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()
# создание таблиц в БД, если их нет
create_tables(cursor=cursor, connection=connection)


async def fetch(params):
    """получение прогноза по параметрам с open-meteo"""

    async with aiohttp.ClientSession() as session:
        async with session.get(OPEN_METEO_URL, params=params) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch weather data")
            data = await response.json()
            current_weather = data.get("current", {})
            return data


@app.post("/weather_info/{latitude, longitude}")
async def get_weather_now(request: WeatherRequest):
    """получение погоды по координатам сейчас"""

    params = {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "current": ["temperature_2m", "surface_pressure", "wind_speed_10m"]
    }
    weather = await fetch(params=params)
    current_weather = weather.get("current", {})
    return {
        "temperature": current_weather.get("temperature_2m"),
        "wind_speed": current_weather.get("wind_speed_10m"),
        "pressure": current_weather.get("surface_pressure")
    }


@app.post("/city_info/city_monitoring/{city_name, latitude, longitude, user_id}")
async def add_city(request: CityMonitorRequest):
    """добавление города в БД для его доступности/сохранения прогноза"""

    user = get_user_by_id(cursor=cursor, user_id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    params = {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "minutely_15": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "start_date": formatted_date,
        "end_date": formatted_date
    }
    weather_info = await fetch(params=params)
    post_city_data(cursor=cursor, connection=connection, request=request, weather_info=weather_info)
    return {"message": "City added successfully"}


@app.get("/city_info/city_availability/{user_id}")
def city_availability(user_id: int):
    """по user_id получить список доступных для просмотра погоды городов"""

    user = get_user_by_id(cursor=cursor, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cities = get_cities(cursor=cursor, user_id=user_id)
    return [{"name": city[0], "latitude": city[1], "longitude": city[2]} for city in cities]



@app.post(
    "/weather_info/current_city_weather/{name, user_id, time, is_temperature, is_humidity, is_wind_speed, "
    "is_precipitation}")
def post_city_weather(request: TimeWeatherRequest):
    """получение погоды сегодня в городе (по названию) в определенное время"""

    user = get_user_by_id(cursor=cursor, user_id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    city = get_city_by_name_and_user(cursor=cursor, city_name=request.name, user_id=request.user_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    data = json.loads(city[5])  # получение данных о городе
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    time_today = f"{formatted_date}T{request.time[:2]}:{int(request.time[3:]) - int(request.time[3:]) % 15}"  # подгон под интервал в 15 минут
    minute_weather = data["minutely_15"]
    index_to_use = minute_weather["time"].index(time_today)
    answer = {}

    # параметры для вывода
    if request.is_precipitation:
        answer["precipitation"] = minute_weather["precipitation"][index_to_use]
    if request.is_humidity:
        answer["humidity"] = minute_weather["relative_humidity_2m"][index_to_use]
    if request.is_temperature:
        answer["temperature"] = minute_weather["temperature_2m"][index_to_use]
    if request.is_wind_speed:
        answer["wind_speed"] = minute_weather["wind_speed_10m"][index_to_use]
    return answer


@app.post("/users/register/{name}")
def register_user(request: RegisterUserRequest):
    """регистрация нового пользователя по имени"""

    try:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (request.name,))
        connection.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "name": request.name}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


if __name__ == "__main__":
    uvicorn.run("script:app", reload=True, host="127.0.0.1", port=8000)  # main loop
