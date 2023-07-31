import time
import json
import requests

two_hours_adr = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
twenty_four_hours_adr = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
four_days_adr = "https://api.data.gov.sg/v1/environment/4-day-weather-forecast"

response = requests.get(four_days_adr)


if response.status_code==200:
    # print(json.dumps(response.json(), indent=4))
    print(response.json().get('items')[0].get('forecasts')[0].get('date') + ": " + response.json().get('items')[0].get('forecasts')[0].get('forecast'))
else:
    print("Error receiving data.")
