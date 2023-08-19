import time
import json
import requests

two_hours_adr = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
twenty_four_hours_adr = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
four_days_adr = "https://api.data.gov.sg/v1/environment/4-day-weather-forecast"

response = requests.get(twenty_four_hours_adr)
if response.status_code==200:
    # print(json.dumps(response.json(), indent=4))
    for i in [0,1,2]:
        start_time = requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][i]['time']['start'][:16]
        end_time = requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][i]['time']['end'][11:16]
        region_weather = ""
        for k,v in requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][i]['regions'].items():
            region_weather += f"{str(k)}: {v}\n"
        print(
            f"{start_time}-{end_time}: \n{region_weather}"
        )
else:
    print("Error receiving data.")

response = requests.get(four_days_adr)
if response.status_code==200:
    # print(json.dumps(response.json(), indent=4))
    print(
        response.json().get('items')[0].get('forecasts')[0].get('date') + ": " + response.json().get('items')[0].get('forecasts')[0].get('forecast')
    )
else:
    print("Error receiving data.")
