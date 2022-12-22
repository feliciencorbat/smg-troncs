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
    year_species_maillettes = year_species_maillettes[["Espèce", "Espèce actuelle", "Liste rouge"]].drop_duplicates().sort_values('Espèce')
    year_species_bossy = year_species_bossy[["Espèce", "Espèce actuelle", "Liste rouge"]].drop_duplicates().sort_values('Espèce')
    year_species_isole = year_species_isole[["Espèce", "Espèce actuelle", "Liste rouge"]].drop_duplicates().sort_values('Espèce')

    # Retirer les anciennes espèces
    new_species_maillettes = pd.merge(year_species_maillettes, old_species_maillettes, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1).reset_index(drop=True)
    new_species_bossy = pd.merge(year_species_bossy, old_species_bossy, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1).reset_index(drop=True)
    new_species_isole = pd.merge(year_species_isole, old_species_isole, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1).reset_index(drop=True)

    return new_species_maillettes, new_species_bossy, new_species_isole