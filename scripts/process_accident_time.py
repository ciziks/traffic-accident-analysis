from datetime import datetime, timedelta
import pandas as pd


# Encontra a hora mais próxima do acidente
def round_hour(row: pd.Series):
    # Concatenando data e hora do acidente
    full_date: str = f'{row["data_inversa"]} {row["horario"]}'
    full_datetime: datetime = datetime.strptime(full_date, "%m/%d/%Y %H:%M:%S")

    delta = timedelta(hours=full_datetime.minute // 30)
    rounded_datetime = (
        full_datetime.replace(
            second=0, microsecond=0, minute=0, hour=full_datetime.hour
        )
        + delta
    )

    return datetime.strftime(rounded_datetime, "%d/%m/%Y %H:%M:%S")


# Coletando dados de acidentes de trânsito da PRF
datatran_df = pd.read_csv("raw_prf_data/datatran_2022.csv")

# Aplicando função que arredonda data e hora do acidente
datatran_df["rounded_datetime"] = datatran_df.apply(round_hour, axis=1)

# Salvando arquivo como csv
datatran_df.to_csv("processed_prf_data/prf_with_datetime.csv")
