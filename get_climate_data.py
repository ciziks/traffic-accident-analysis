from pprint import pprint
import requests

# !https://open-meteo.com/en/docs/historical-weather-api
# URL Base da API Open-Meteo
url = "https://archive-api.open-meteo.com/v1/archive"

# Variáveis metereológicas de interesse ao problema
climate_variables = [
    "rain",
    "temperature_2m",
    "apparent_temperature",
    "relativehumidity_2m",
    "cloudcover",
    "windspeed_10m",
    "is_day",
]

# Parâmetros da requisição
params = {
    "latitude": "-7.43280012",
    "longitude": "-40.68261908",
    "start_date": "2022-01-01",
    "end_date": "2022-01-01",
    "hourly": ",".join(climate_variables),
}

# Requisitando informações com método GET
response = requests.get(url, params)

# Printando resposta da API
pprint(response.json())