from rest_framework import status
from weather_app.models import CityWeather
from rest_framework.views import APIView
import requests
from weather_checker.settings import OWM_API_KEY, WEATHER_DATA_LIFETIME
from django.utils import timezone
from rest_framework.response import Response

class CityWeatherView(APIView):

    def get(self, request, city):
        city_entry = CityWeather.objects.filter(city=city).first()
        if city_entry:
            lifetime = timezone.now() - city_entry.last_update
            if lifetime <= WEATHER_DATA_LIFETIME:
                return Response(city_entry.weather_data, status=status.HTTP_200_OK)
        weather_api_rsp = requests.get(
            url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric',
        )
        if weather_api_rsp.status_code != 200:
            return Response(weather_api_rsp.text, status=weather_api_rsp.status_code)
        if city_entry:
            city_entry.weather_data = weather_api_rsp.json()
            city_entry.save()
        else:
            new_entry = CityWeather()
            new_entry.city = city
            new_entry.weather_data = weather_api_rsp.json()
            new_entry.save()
        return Response(weather_api_rsp.json(), status=status.HTTP_200_OK)
