from pydantic import BaseModel

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherRequest(BaseModel):
    """запрос для получения погоды сейчас"""

    latitude: float
    longitude: float


class CityMonitorRequest(BaseModel):
    """запрос для добавления города в список доступных пользователя и его дальнейшего мониторинга"""

    name: str
    latitude: float
    longitude: float
    user_id: int


class RegisterUserRequest(BaseModel):
    """запрос для регистрации пользователя"""

    name: str


class TimeWeatherRequest(BaseModel):
    """запрос для получения погоды на заданное время в городе сегодня"""

    name: str
    user_id: int
    time: str
    is_temperature: bool
    is_humidity: bool
    is_wind_speed: bool
    is_precipitation: bool
