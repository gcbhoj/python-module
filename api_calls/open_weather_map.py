import os

import requests

from models.weather_data import WeatherData


class GetCurrentWeatherData:

    DEFAULT_LATITUDE = 43.7315
    DEFAULT_LONGITUDE = -79.7624

    def __init__(
        self,
        latitude=None,
        longitude=None
    ):
        self.api_key = os.getenv("OPEN_WEATHER_API")

        if not self.api_key:
            raise ValueError(
                "Open Weather Map API Key Not Available"
            )

        self.latitude = (
            latitude
            if latitude is not None
            else self.DEFAULT_LATITUDE
        )

        self.longitude = (
            longitude
            if longitude is not None
            else self.DEFAULT_LONGITUDE
        )

    def get_weather_report(self):

        api_response = self._send_request(
            self.latitude,
            self.longitude
        )

        return self._extract_data(
            api_response
        )

    def _send_request(
        self,
        latitude,
        longitude
    ):

        url = (
            "https://api.openweathermap.org/data/4.0/"
            "onecall/timeline/1day"
        )

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def _extract_data(self, data):

        forecast_data = data.get("data",[])

        if not forecast_data:
            raise ValueError("Weather data not available")

        current_weather = forecast_data[0]

        temperature = current_weather.get( "temp",{}).get(
            "day"
        )

        feels_like = current_weather.get(
            "feels_like",
            {}
        ).get(
            "day"
        )

        weather = current_weather.get(
            "weather",
            [{}]
        )[0]

        return WeatherData(
            temperature=temperature,
            feels_like=feels_like,
            humidity=current_weather.get(
                "humidity"
            ),
            pressure=current_weather.get(
                "pressure"
            ),
            wind_speed=current_weather.get(
                "wind_speed"
            ),
            wind_direction=current_weather.get(
                "wind_deg"
            ),
            condition=weather.get(
                "main"
            ),
            description=weather.get(
                "description"
            )
        )