import pandas as pd

def rare_species_lists(data: pd.DataFrame, year):

    # Filtrer année
    data_year = data.loc[data["Année"] == int(year)]

    # Filtrer menace
    data_threat = data_year.loc[data["Menace"] == "Menacé"]

    # Filtrer lieu
    data_maillettes = data_threat.loc[data["Lieu"] == "Les Maillettes"]
    data_bossy = data_threat.loc[data["Lieu"] == "Bossy"]

    # Filtrer les colonnes
    data_maillettes = data_maillettes[["Espèce", "Espèce actuelle", "Liste rouge"]].drop_duplicates().sort_values('Espèce')
    data_bossy = data_bossy[["Espèce", "Espèce actuelle", "Liste rouge"]].drop_duplicates().sort_values('Espèce')

    return data_maillettes, data_bossy
