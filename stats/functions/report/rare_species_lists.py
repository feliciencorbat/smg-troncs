import numpy as np
import pandas as pd

def rare_species_lists(data: pd.DataFrame, year):

    # Filtrer année
    data_year = data.loc[data["Année"] == int(year)]

    # Filtrer menace
    data_threat = data_year.loc[data["Menace"] == "Menacé"]

    # Filtrer lieu
    data_maillettes = data_threat.loc[data["Lieu"] == "Les Maillettes"]
    data_bossy = data_threat.loc[data["Lieu"] == "Bossy"]
    data_bossy = data_bossy.loc[data["Tronc"] != "isolé"]
    data_isole = data_threat.loc[data["Tronc"] == "isolé"]

    # Filtrer les colonnes
    data_maillettes = data_maillettes[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Menace"]].drop_duplicates().sort_values('Espèce')
    data_bossy = data_bossy[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Menace"]].drop_duplicates().sort_values('Espèce')
    data_isole = data_isole[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Menace"]].drop_duplicates().sort_values('Espèce')

    # Group by Tronc
    data_maillettes = data_maillettes[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Menace"]].groupby(by=["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Menace"], dropna=False).agg({'Tronc' : ', '.join}).reset_index().reindex(columns=data_maillettes.columns)
    data_bossy = data_bossy[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Menace"]].groupby(by=["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Menace"], dropna=False).agg({'Tronc' : ', '.join}).reset_index().reindex(columns=data_bossy.columns)

    return data_maillettes, data_bossy, data_isole
