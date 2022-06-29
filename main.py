import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})


api_key = "enter api key here"
LAT = "enter latitude as float"
LONG = "enter latitude as float"
api = "https://api.openweathermap.org/data/2.5/onecall"
auth_token = "enter auth token here"
account_sid = "enter acct sid here"
weather_parameters = {
    "appid": api_key,
    "lat": LAT,
    "lon": LONG,
    "exclude": "current,minutely,daily",
    "units": "imperial"
}

response = requests.get(api, params=weather_parameters)
response.raise_for_status()
data = response.json()


bad_weather = False
twelve_hours = data["hourly"][:12]
for hour in twelve_hours:
    weather_code = int(hour["weather"][0]["id"])
    if weather_code < 700:
        bad_weather = True


if bad_weather:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Bad weather incoming today! Remember to bring an Umbrella ☔️",
        from_='enter twilio phone # here',
        to='enter your phone # here'
    )

    print(message.status)
