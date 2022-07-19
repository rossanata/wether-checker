from weather_app.models import CityWeather
import requests
from weather_checker.settings import OWM_API_KEY
from celery import shared_task


@shared_task
def update_weather_data_daily():
   city_entries = CityWeather.objects.all()
   for city_entry in city_entries:
       weather_api_rsp = requests.get(
           url=f'https://api.openweathermap.org/data/2.5/weather?q={city_entry.city}&appid={OWM_API_KEY}&units=metric',
       )
       city_entry.weather_data = weather_api_rsp.json()
       city_entry.save()
