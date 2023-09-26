import pandas as pd

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
df_temps[df_temps["Ano"] == "-"] = df_temps[df_temps["Ano"] == "-"].apply(calculate_missing_years, axis=1)

# Realizando merge dos Dataframes
df_inmet = df_temps[["Nome da Estação", "Ano"]].merge(df_stations[["Nome da Estação", "Latitude", "Longitude", "UF"]], how='inner', on='Nome da Estação')

# Salvando como CSV
df_inmet.to_csv("processed_data/inmet_data.csv")