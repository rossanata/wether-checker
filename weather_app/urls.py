from django.urls import path, include
from weather_app.views import CityWeatherView

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('check-by-city/<str:city>/', CityWeatherView.as_view()),
]
