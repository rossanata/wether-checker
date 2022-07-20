from datetime import timedelta
from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from weather_app.views import CityWeatherView


class ViewTestCase(SimpleTestCase):
    VIEW_PATH = 'weather_app.views'

    @patch(f'{VIEW_PATH}.Response')
    @patch(f'{VIEW_PATH}.CityWeather')
    @patch(f"{VIEW_PATH}.timezone")
    @patch(f"{VIEW_PATH}.WEATHER_DATA_LIFETIME", timedelta(hours=4))
    def test_city_weather_get_city_entry_not_expired(
        self,
        timezone_patch,
        city_weather_model_patch,
        response_model_patch,
    ):
        city_name_mock = MagicMock()
        city_weather_model_mock = MagicMock(last_update = timedelta(hours=1))
        city_weather_model_patch.objects.filter().first.return_value = city_weather_model_mock
        timezone_patch.now.return_value = timedelta(hours=4, minutes=59)
        response_mock = MagicMock()
        response_model_patch.return_value = response_mock
        request_mock = MagicMock()

        response = CityWeatherView().get(request_mock, city=city_name_mock)

        city_weather_model_patch.objects.filter.assert_called_with(city=city_name_mock)
        city_weather_model_patch.objects.filter().first.assert_called_once()

        self.assertEqual(response, response_mock)

    @patch(f'{VIEW_PATH}.requests')
    @patch(f'{VIEW_PATH}.Response')
    @patch(f'{VIEW_PATH}.CityWeather')
    @patch(f"{VIEW_PATH}.timezone")
    @patch(f"{VIEW_PATH}.WEATHER_DATA_LIFETIME", timedelta(hours=4))
    @patch(f"{VIEW_PATH}.OWM_API_KEY", 'test_api_key')
    def test_city_weather_get_city_entry_expired(
        self,
        timezone_patch,
        city_weather_model_patch,
        response_model_patch,
        requests_patch,
    ):
        city_name_mock = 'MagicMock()'
        city_weather_model_mock = MagicMock(last_update = timedelta(hours=1), weather_data = 'initial data')
        city_weather_model_patch.objects.filter().first.return_value = city_weather_model_mock
        timezone_patch.now.return_value = timedelta(hours=5, minutes=1)
        response_mock = MagicMock()
        response_model_patch.return_value = response_mock
        request_mock = MagicMock()
        requests_mock = MagicMock(status_code=200)
        requests_patch.get.return_value = requests_mock
        requests_mock.json.return_value = 'new_data'

        response = CityWeatherView().get(request_mock, city=city_name_mock)

        requests_patch.get.assert_called_with(url=f'https://api.openweathermap.org/data/2.5/weather?q={city_name_mock}&appid=test_api_key&units=metric',)
        city_weather_model_patch.objects.filter.assert_called_with(city=city_name_mock)
        city_weather_model_patch.objects.filter().first.assert_called_once()
        self.assertEqual(city_weather_model_mock.weather_data, 'new_data')
        city_weather_model_mock.save.assert_called_once()
        self.assertEqual(response, response_mock)

# TODO: finish the rest of the tests

    def test_city_weather_get_weather_api_rsp_not_200(self):
        pass

    def test_city_weather_get_weather_api_rsp_200_city_entry(self):
        pass

    def test_city_weather_get_weather_api_rsp_200_new_entry(self):
        pass
