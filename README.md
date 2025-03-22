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

Скрипт запускается из script.py

Зависимости в requirements.txt
