# Weather Checker

This is an API that lets the user check the current weather in a city by city name.

A request to Open Weather Map API for the current weather data for one location can be made, by providing a city name.
Data is fetched from Open Weather Map API or from our DB in case a query for the same city was already made in the last 4 hours.


## Technologies Used

- Python
- Django Framework
- Postgresql Database
- Celery
- Swagger (drf-yasg)
- Token Authorization
- Third party integration - Open Weather Map API (https://openweathermap.org/current)


## Run Locally

Clone the project

```bash
  git clone https://github.com/rossanata/wether-checker.git
```

Go to the project directory

```bash
  cd wether-checker
```

Install packages and dependencies

```bash
  pip install -r requirements.txt
```

Go to Open Weather Map API (https://openweathermap.org/current) and create an account (API key will be generated for you) in order to be able to fetch data from the API. Bear in mind that account activation might take a few hours, so your key might not work straight away

Create .env file, copy the listed global variables from env.template and populate accordingly

Start the server

```bash
  python manage.py runserver
```

Start the worker process with scheduler (for periodic update of the weather data)

```bash
  celery -A weather_checker worker -B -l INFO
```

Make sure you generate a token and insert it when making requests


## Usage

Register a user on '/weather/auth/registration/'

Log in the user on '/weather/auth/login/'

Copy the token provided in the response body:

    {
    "key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

Make a GET request using the acquired token on '/weather/check-by-city/<name_of_the_city>/'

Token format to be used for the request:

    Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Detailed information of current weather in the city will be received in the following format:

     {
     "coord": {
       "lon": -0.13,
       "lat": 51.51
     },
     "weather": [
       {
         "id": 300,
         "main": "Drizzle",
         "description": "light intensity drizzle",
         "icon": "09d"
       }
     ],
     "base": "stations",
     "main": {
       "temp": 280.32,
       "pressure": 1012,
       "humidity": 81,
       "temp_min": 279.15,
       "temp_max": 281.15
     },
     "visibility": 10000,
     "wind": {
       "speed": 4.1,
       "deg": 80
     },
     "clouds": {
       "all": 90
     },
     "dt": 1485789600,
     "sys": {
       "type": 1,
       "id": 5091,
       "message": 0.0103,
       "country": "GB",
       "sunrise": 1485762037,
       "sunset": 1485794875
     },
     "id": 2643743,
     "name": "London",
     "cod": 200
     }


## Technical Decisions

django-rest-auth has been integreated in Weather Checker to use its out-of-the-box authorization and authentication functionalities

- /weather/auth/login/ (POST)
- /weather/auth/logout/ (POST)
- /weather/auth/password/change/ (POST)
- /weather/auth/registration/ (POST)
- /weather/auth/user/ (GET, PUT, PATCH)

Swagger integration facilitates the following endpoints

- JSON view of API specification at /swagger.json
- YAML view of API specification at /swagger.yaml
- swagger-ui view of API specification at /swagger/
- ReDoc view of API specification at /redoc/

Open Weather Map API integration - ideas for future improvements

- results in different units of measurement could be added in case of future interest
- even when inaccurate spelling (e.g. Burgas, Bourgas) or cyrillic/latin letters (e.g. Sofia, София) are used for one and the same city name, the third party sends back one and the same data (with the same city ID in the json), saving process might be optimized to avoid DB entries repetition
