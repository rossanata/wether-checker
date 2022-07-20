from django.urls import path, include
from weather_app.views import CityWeatherView
from rest_auth import urls as rest_auth_urls
from rest_auth.registration import urls as rest_auth_registration_urls


rest_auth_filtered_urls = [
    url for url in rest_auth_urls.urlpatterns if 
        url.name == 'rest_login' or
        url.name == 'rest_logout' or
        url.name == 'rest_password_change' or
        url.name == 'rest_user_details'
]

rest_register_url = [url for url in rest_auth_registration_urls.urlpatterns if url.name == 'rest_register']

urlpatterns = [
    path('auth/', include(rest_auth_filtered_urls)),
    path('auth/registration/', include(rest_register_url)),
    path('check-by-city/<str:city>/', CityWeatherView.as_view()),
]
