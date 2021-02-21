import pandas as pd
import pickle
from calendar import monthrange
from datetime import datetime

# This script expects the SRAG .csv's from 2009-2020
# to be in folder data/, named as 'SRAG {year}.csv'.
# Death by year information will be exported to 'data/srag_deaths_by_year.data', with pickle.
# SRAG .csv files can be downloaded from the Ministry of Health of Brazil opendata website:
# https://opendatasus.saude.gov.br/dataset/bd-srag-2009-a-2012
# https://opendatasus.saude.gov.br/dataset/bd-srag-2012-a-2018
# https://opendatasus.saude.gov.br/dataset/bd-srag-2019
# https://opendatasus.saude.gov.br/dataset/bd-srag-2020
# https://opendatasus.saude.gov.br/dataset/bd-srag-2021

# Returns a list of all dates   
# represented as strings 'dd/mm/YYYY', e.g.: '25/03/2010'
def all_dates(year):
    dates = []
    for month in range(1, 12 + 1):
        for day in range(1, monthrange(year, month)[1] + 1):
            str_day = str(day).rjust(2, '0')
            str_month = str(month).rjust(2, '0')
            dates.append(f"{str_day}/{str_month}/{year}")
    return dates


def evolution_from_csv(csv):
    df = pd.read_csv(csv, sep=";", error_bad_lines=False, encoding="ISO-8859-1", low_memory=False)

    # Older files use 'DT_OBITO' instead of 'DT_EVOLUCA'.
    if "DT_OBITO" in df.columns:
        df.rename(columns={"DT_OBITO": "DT_EVOLUCA"}, inplace=True)

    df = df[["EVOLUCAO", "DT_EVOLUCA"]]
    df = df[df["EVOLUCAO"] == 2]

    null_dt_count = df["DT_EVOLUCA"].isna().value_counts()
    if True not in null_dt_count:
        null_dt_count[True] = 0

    print(f"File {csv} had {null_dt_count[True]} null dates in deaths. Ignoring these...")
    return df.groupby("DT_EVOLUCA")["EVOLUCAO"].count()


def deaths_in_year(year):
    file = f"data/SRAG {year}.csv"
    df_group = evolution_from_csv(file)
    dates_year = all_dates(year)

    deaths = []
    for data in dates_year:
        if data in df_group:
            deaths.append(df_group[data])
        else:
            deaths.append(0)

    plt_dates = [datetime.strptime(date, "%d/%m/%Y").date() for date in dates_year]
    return plt_dates, deaths


if __name__ == '__main__':
    years_info = []

    for year in range(2009, 2020 + 1):
        plt_dates, deaths = deaths_in_year(year)
        years_info.append([year, plt_dates, deaths])

    with open("data/srag_deaths_by_year.data", "wb") as file:
        pickle.dump(years_info, file)
