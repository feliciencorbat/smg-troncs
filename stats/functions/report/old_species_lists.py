import pandas as pd

def old_species_lists(data: pd.DataFrame, year):

    # Filtrer année
    old_species = data.loc[data["Année"] < int(year)]

    # Filtrer lieu
    old_species_maillettes = old_species.loc[data["Lieu"] == "Les Maillettes"]
    old_species_bossy = old_species.loc[data["Lieu"] == "Bossy"]
    old_species_bossy = old_species_bossy.loc[data["Tronc"] != "isolé"]
    old_species_isole = old_species.loc[data["Tronc"] == "isolé"]

    # Filtrer les colonnes
    old_species_maillettes = old_species_maillettes[["Espèce"]].drop_duplicates().sort_values('Espèce')
    old_species_bossy = old_species_bossy[["Espèce"]].drop_duplicates().sort_values('Espèce')
    old_species_isole = old_species_isole[["Espèce"]].drop_duplicates().sort_values('Espèce')

    return old_species_maillettes, old_species_bossy, old_species_isole
