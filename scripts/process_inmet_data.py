import pandas as pd
import math

# Meses do Ano
months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

# Coletando dados da localização das estações e as médias anuais registradas pelo INMET
df_stations = pd.read_csv("raw_data/inmet_stations.csv", index_col=0)
df_temps = pd.read_csv("raw_data/inmet_temperature.csv", index_col=0)


# Função para calcular a média anual com base nos meses disponíveis
def calculate_missing_years(row):
    mean_months = 0
    num_months = 0

    for m in months:
        if row[m] != "-":
            mean_months += float(row[m])
            num_months += 1

    row["Ano"] = round(mean_months / num_months, 1)

    return row


# Calculando média dos dados ausentes
df_temps[df_temps["Ano"] == "-"] = df_temps[df_temps["Ano"] == "-"].apply(
    calculate_missing_years, axis=1
)

# Realizando merge dos Dataframes
df_inmet = df_temps[["Nome da Estação", "Ano"]].merge(
    df_stations[["Nome da Estação", "Latitude", "Longitude", "UF"]],
    how="inner",
    on="Nome da Estação",
)

# Salvando como CSV
df_inmet.to_csv("processed_data/inmet_data.csv")


# Adicionando Temperatura média por região nos Dados da PRF
def calcular_distancia(lat1, lon1, lat2, lon2):
    # Raio da Terra em km
    raio_terra = 6371.0

    # Converter latitudes e longitudes de graus para radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferença de latitude e longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Aplicar a fórmula de Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calcular a distância
    distancia = raio_terra * c
    return distancia


# Recuperando dados da PRF de Chuva
df_rain = pd.read_csv("processed_data/prf_rain_data.csv", index_col=0)


# Armazenando média das temperaturas em cada local de acidente
def mean_temp(row):
    temperature = ""
    low_distance = 999999999999999

    for index, temp_row in df_inmet.iterrows():
        # Calculando distância
        distance = calcular_distancia(
            row["latitude"],
            row["longitude"],
            temp_row["Latitude"],
            temp_row["Longitude"],
        )

        # Verificando se é a estação mais próxima do local
        if distance < low_distance:
            low_distance = distance
            temperature = temp_row["Ano"]

    row["mean_temperature"] = temperature

    return row


# Aplicando no Dataframe da PRF
df = df_rain.apply(mean_temp, axis=1)

# Salvando como CSV
df.to_csv("processed_data/prf_inmet_rain_data.csv")
