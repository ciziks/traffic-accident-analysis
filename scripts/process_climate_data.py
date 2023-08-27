import pandas as pd
import requests
from datetime import datetime

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


# !https://open-meteo.com/en/docs/historical-weather-api
# Função que recupera informações do clima através da API Open-Meteo
def get_climate_info(row: pd.Series):
    # Capturando horário do acidente arredondado
    date = datetime.strptime(row["rounded_datetime"], "%d/%m/%Y %H:%M:%S")
    hour = int(date.strftime("%H"))

    # Parâmetros da requisição
    params = {
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "start_date": date.strftime("%Y-%m-%d"),
        "end_date": date.strftime("%Y-%m-%d"),
        "timezone": "America/Sao_Paulo",
        "hourly": ",".join(climate_variables),
    }

    # Requisitando informações com método GET
    response = requests.get(url, params)

    # Coletando resposta da API
    response_json = response.json()

    # Coletando métricas do clima
    climate_metrics = response_json["hourly"]

    # Capturando dados do clima do horário do acidente
    climate_data = [climate_metrics[var][hour] for var in climate_variables]

    return pd.Series(climate_data)


# Coletando dados de acidentes de trânsito da PRF
datatran_df = pd.read_csv("processed_prf_data/prf_with_datetime.csv")

# Coletando acidentes que possuem como causa principal a Chuva
df_rain = datatran_df[datatran_df["causa_acidente"] == "Chuva"]

# Coletando mesmo número de acidentes aleatórios que não possuem como causa a chuva
df_not_rain = datatran_df[datatran_df["causa_acidente"] != "Chuva"].sample(
    n=len(df_rain),
    random_state=42,
)

# Cruzando dados climáticos com acidentes causados por chuva
df_rain[climate_variables] = df_rain.apply(get_climate_info, axis=1)
df_rain.drop(["Unnamed: 0"], axis=1, inplace=True)

# Cruzando dados climáticos com acidentes causados por chuva
df_not_rain[climate_variables] = df_not_rain.apply(get_climate_info, axis=1)
df_not_rain.drop(["Unnamed: 0"], axis=1, inplace=True)

# Salvando dados cruzados em CSV
df_rain.to_csv("processed_prf_data/prf_rain_data.csv")
df_not_rain.to_csv("processed_prf_data/prf_not_rain_data.csv")
