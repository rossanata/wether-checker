from django.db import models

class CityWeather(models.Model):
    city = models.CharField(max_length=100, unique=True)
    last_update = models.DateTimeField(auto_now=True)
    weather_data = models.JSONField()
