import pandas as pd

def new_species_lists(data: pd.DataFrame, old_species_maillettes, old_species_bossy, old_species_isole, year):

    # Filtrer l'année
    year_species = data.loc[data["Année"] == int(year)]

    # Filtrer le lieu
    year_species_maillettes = year_species.loc[data["Lieu"] == "Les Maillettes"]
    year_species_bossy = year_species.loc[data["Lieu"] == "Bossy"]
    year_species_bossy = year_species_bossy.loc[data["Tronc"] != "isolé"]
    year_species_isole = year_species.loc[data["Tronc"] == "isolé"]

    # Filtrer les colonnes
    year_species_maillettes = year_species_maillettes[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Fréquence"]].drop_duplicates().sort_values('Espèce')
    year_species_bossy = year_species_bossy[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Fréquence"]].drop_duplicates().sort_values('Espèce')
    year_species_isole = year_species_isole[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Fréquence"]].drop_duplicates().sort_values('Espèce')

    # Group by Tronc
    year_species_maillettes = year_species_maillettes[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Fréquence"]].groupby(
        by=["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Fréquence"], dropna=False).agg({'Tronc': ', '.join}).reset_index().reindex(
        columns=year_species_maillettes.columns)
    year_species_bossy = year_species_bossy[["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Tronc", "Fréquence"]].groupby(
        by=["Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Liste rouge", "Fréquence"], dropna=False).agg({'Tronc': ', '.join}).reset_index().reindex(
        columns=year_species_bossy.columns)

    # Retirer les anciennes espèces
    new_species_maillettes = pd.merge(year_species_maillettes, old_species_maillettes, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1).reset_index(drop=True)
    new_species_bossy = pd.merge(year_species_bossy, old_species_bossy, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1).reset_index(drop=True)
    new_species_isole = pd.merge(year_species_isole, old_species_isole, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1).reset_index(drop=True)

    total_species_maillettes = old_species_maillettes.shape[0] + new_species_maillettes.shape[0]
    total_species_bossy = old_species_bossy.shape[0] + new_species_bossy.shape[0]
    total_species_isole = old_species_isole.shape[0] + new_species_isole.shape[0]

    return new_species_maillettes, new_species_bossy, new_species_isole, total_species_maillettes, total_species_bossy, total_species_isole
