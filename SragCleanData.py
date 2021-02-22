import pandas as pd
import numpy as np
import SragConstants as C
import time

# Expects "data/SRAG 2020.csv".
# SRAG .csv files can be downloaded from the Ministry of Health of Brazil opendata website:
# https://opendatasus.saude.gov.br/dataset/bd-srag-2020
# This script will clean this file and export as "data/SRAG 2020_cleaned.csv".


# Filters data
def cleaned_data(file_name):
    start_time = time.time()

    df = pd.read_csv(file_name, sep=";", error_bad_lines=False, encoding="ISO-8859-1")
    df = df[C.WANTED_COLUMNS]  # Select only columns we will use

    print(f"Loaded file contains {df.shape[0]} entries.")

    print(f"Dropping {df[df['CLASSI_FIN'] != C.CLASSI_FIN.COVID_19.value].shape[0]} entries NOT COVID_19.")
    df = df[df["CLASSI_FIN"] == C.CLASSI_FIN.COVID_19.value]  # only covid19

    print(f"Dropping {df[df['CS_SEXO'] == C.CS_SEXO.IGNORADO.value].shape[0]} entries with ignored SEXO.")
    df = df[df["CS_SEXO"] != C.CS_SEXO.IGNORADO.value]  # sexo must not be ignored

    print(f"Dropping {df[df['EVOLUCAO'] == C.EVOLUCAO.IGNORADO.value].shape[0]} entries with ignored EVOLUCAO.")
    df = df[df["EVOLUCAO"] != C.EVOLUCAO.IGNORADO.value]  # Evolucao must not be ignored

    print(f"Dropping {df[df['EVOLUCAO'] == 3].shape[0]} entries with EVOLUCAO = 3.")
    df = df[df["EVOLUCAO"] != C.EVOLUCAO.OUTRA_CAUSA.value]  # Evolucao must not be ignored

    print(f"Dropping {df[df['TP_IDADE'] != C.TP_IDADE.ANOS.value].shape[0]} entries with tipo idade not anos.")
    df = df[df["TP_IDADE"] == C.TP_IDADE.ANOS.value]  # only age >= 1 year

    print(f"Dropping {df[df['NU_IDADE_N'] == 0].shape[0]} entries with age 0.")
    df = df[df["NU_IDADE_N"] != 0]  # only age >= 1 year

    before = df.shape[0]
    df.dropna(subset=["CS_SEXO"], how="any", inplace=True)
    after = df.shape[0]
    print(f"Dropping {before-after} entries with NULL CS_SEXO")

    before = df.shape[0]
    df.dropna(subset=["NU_IDADE_N"], how="any", inplace=True)
    after = df.shape[0]
    print(f"Dropping {before-after} entries with NULL NU_IDADE_N")

    before = df.shape[0]
    df.dropna(subset=["TP_IDADE"], how="any", inplace=True)
    after = df.shape[0]
    print(f"Dropping {before-after} entries with NULL TP_IDADE")

    before = df.shape[0]
    df.dropna(subset=["CLASSI_FIN"], how="any", inplace=True)
    after = df.shape[0]
    print(f"Dropping {before-after} entries with NULL CLASSI_FIN")

    before = df.shape[0]
    df.dropna(subset=["EVOLUCAO"], how="any", inplace=True)
    after = df.shape[0]
    print(f"Dropping {before-after} entries with NULL EVOLUCAO")

    # Convert some columns to int
    for column in C.CONVERT_TO_INT_COLUMNS:
        df[column] = df[column].astype(int)

    print(f"Data cleaned: {df.shape[0]} entries.")

    # Define age intervals used
    buckets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 150]
    df['age'] = pd.cut(df['NU_IDADE_N'], buckets)

    print(f"'cleaned_data' took {(time.time() - start_time):.2f} seconds.")

    return df


def process(file_path, nan_to_false=False):
    df = cleaned_data(file_path)

    # These are no longer needed and may cause parsing issues.
    df.drop(columns=["MORB_DESC"], inplace=True)

    if nan_to_false:
        # Convert NaNs in symptoms and comorbidities to false.
        for col in C.SYMPTOMS_AND_COMORBIDITIES:
            df.loc[df[col].isna(), col] = 2

    # Save it as CSV
    new_path = file_path.replace(".csv", "_cleaned.csv")
    print(f"Exporting {df.shape} entries as {new_path}.")
    df.to_csv(new_path, index=False, header=True, sep=";")


if __name__ == '__main__':
    file_path = "data/SRAG 2020.csv"
    process(file_path)
