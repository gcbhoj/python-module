from dataclasses import dataclass


@dataclass
class WeatherData:

    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    condition: str
    description: str