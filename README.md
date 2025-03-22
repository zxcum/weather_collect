# Сбор данных о погоде с открытого API

## get_weather_now
Принимает:
```
    latitude: float
    longitude: float
```
Отдает:
```
{
  "temperature":   float,
  "wind_speed":    float,
  "pressure":      float
}
```
Метод позволяет получпть погоду в данный момент времени по координатам

## add_city
Принимает:
```
    name: str
    latitude: float
    longitude: float
    user_id: int
```
Отдает:
```
    {"message": "City added successfully"}
```
Метод добавляет в БД город, id пользователя, к которому относится город и прогноз погоды на весь день

## city_availability
Принимает:
```
    user_id: int
```
Отдает:
```
    # список в формате:
    {"city": "coords"}
```
По ID пользователя выдает все города, которые ему доступны для запроса прогноза погоды

## post_city_weather
Принимает:
```
    name: str
    user_id: int
    time: str # в формате HH:MM
    is_temperature: bool
    is_humidity: bool
    is_wind_speed: bool
    is_precipitation: bool
```
Отдает:
```
    "temperature":   float,
    "wind_speed":    float,
    "pressure":      float,
    "humidity":      float
```
При обращении подтягивает из БД город и по времени выдает прогноз из имеющихся там данных, можно устанавливать необходимые характеристики (параметры погоды)

## register_user
Принимает:
```
    name: str
```
Отдает:
```
    {"id": user_id, "name": request.name}
```
По ID пользователя выдает все города, которые ему доступны для запроса прогноза погоды

## Итог
В ходе выполнения тестового задания были реализованы 5 методов и взаимодействие с БД (SQLite3), обновление прогноза каждые 15 минут не было реализовано. Также была реализована возможность работы с несколькими пользователями по их ID для методов 2, 3 и 4.

Скрипт запускается из script.py

Зависимости в requirements.txt:

aiohappyeyeballs==2.4.4<br>
aiohttp==3.11.11<br>
aiosignal==1.3.2<br>
annotated-types==0.7.0<br>
anyio==4.8.0<br>
attrs==24.3.0<br>
click==8.1.8<br>
colorama==0.4.6<br>
fastapi==0.115.6<br>
frozenlist==1.5.0<br>
h11==0.14.0<br>
idna==3.10<br>
multidict==6.1.0<br>
propcache==0.2.1<br>
pydantic==2.10.5<br>
pydantic_core==2.27.2<br>
sniffio==1.3.1<br>
starlette==0.41.3<br>
typing_extensions==4.12.2<br>
uvicorn==0.34.0<br>
yarl==1.18.3<br>
