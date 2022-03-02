import json
import urllib.request
import numpy as np
import pandas as pd

"""
Fonction de création d'une liste de données à partir du fichier liste_originale.xls
"""


def new_list(data: pd.DataFrame, export_directory: str, with_gbif: bool) -> None:

    """
    Création colonne Nom binomial
    """
    data["Nom binomial"] = data["Genre"] + " " + data["Espèce"]

    """
    Création colonne Menace
    """
    conditions = [
        (data['LR'] == 'EX'),
        (data['LR'] == 'EW'),
        (data['LR'] == 'RE'),
        (data['LR'] == 'CR'),
        (data['LR'] == 'EN'),
        (data['LR'] == 'VU'),
        (data['LR'] == 'LC'),
        (data['LR'] == 'NT')
    ]
    choices = [
        'Eteint',
        'Eteint',
        'Eteint',
        'Menacé',
        'Menacé',
        'Menacé',
        'Non menacé',
        'Non menacé'
    ]
    data["Menace"] = np.select(condlist=conditions, choicelist=choices, default='Menace inconnue')

    """
    Création colonne Mois
    """
    data['Mois'] = data['Date'].dt.month

    """
    Création colonnes GBIF
    """
    if with_gbif:
        error = pd.DataFrame([], )
        data["GBIF id"] = None
        data["GBIF statut"] = None
        data["GBIF Matching"] = None
        data["GBIF Nom scientifique"] = None
        data["GBIF Nom canonique"] = None
        data["GBIF Phylum"] = None
        data["GBIF Order"] = None
        for row in data.itertuples():
            try:
                name = str(row.Genre) + " " + str(row.Espèce)
                print(name)
                name_url = urllib.parse.quote(name)
                response = urllib.request.urlopen("https://api.gbif.org/v1/species/match?name=" + name_url)

                json_data = response.read().decode("utf-8", "replace")
                gbif_match = json.loads(json_data)
                if gbif_match["rank"] == "SPECIES" or gbif_match["rank"] == "VARIETY" \
                        or gbif_match["rank"] == "SUBSPECIES" or gbif_match["rank"] == "FORM":
                    data.at[row.Index, "GBIF id"] = gbif_match["usageKey"]
                    data.at[row.Index, "GBIF statut"] = gbif_match["status"]
                    data.at[row.Index, "GBIF Matching"] = gbif_match["matchType"]
                    data.at[row.Index, "GBIF Nom scientifique"] = gbif_match["scientificName"]
                    data.at[row.Index, "GBIF Nom canonique"] = gbif_match["canonicalName"]
                    data.at[row.Index, "GBIF Phylum"] = gbif_match["phylum"]
                    data.at[row.Index, "GBIF Order"] = gbif_match["order"]
                else:
                    error_row = pd.DataFrame({'Ligne': [row.Index+2], 'Genre': [row.Genre], 'Espèce': [row.Espèce]})
                    error = pd.concat([error, error_row], ignore_index=True, axis=0)
            except:
                print(row.Genre + " " + row.Espèce + " non récupérée")
                error_row = pd.DataFrame({'Ligne': [row.Index+2], 'Genre': [row.Genre], 'Espèce': [row.Espèce]})
                error = pd.concat([error, error_row], ignore_index=True, axis=0)

        error.to_excel(export_directory + "/liste_modifiee_erreurs.xlsx")

    data.to_excel(export_directory + "/liste_modifiee.xlsx")
