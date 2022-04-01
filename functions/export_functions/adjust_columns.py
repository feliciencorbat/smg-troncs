from typing import Tuple

import pandas as pd


def adjust_columns(data: pd.DataFrame, errors: pd.DataFrame, with_gbif: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Colonne date de type datetime en type date
    data["Date"] = pd.to_datetime(data['Date']).dt.date

    # Renommer les colonnes de data
    data = data.rename(columns={"LR": "Liste rouge", "Substrat": "Tronc", "Espèce du substrat": "Espèce du tronc",
                                "D. moyen": "Diamètre moyen", "Pourriture": "Degré de pourriture"})

    # Garder uniquement les colonnes nécessaires
    if with_gbif:
        data = data[
            ["Date", "Saison", "Mois", "Espèce", "Espèce actuelle", "Phylum", "Ordre", "cf", "Liste rouge", "Menace",
             "Tronc", "Espèce du tronc", "Diamètre moyen", "Longueur", "Degré de pourriture", "Lieu", "Groupe troncs",
             "Date de coupe", "Age du tronc"]]
    else:
        data = data[
            ["Date", "Saison", "Mois", "Espèce", "cf", "Liste rouge", "Menace", "Tronc", "Espèce du tronc",
             "Diamètre moyen", "Longueur", "Degré de pourriture", "Lieu", "Groupe troncs", "Date de coupe",
             "Age du tronc"]]

    errors = errors[["Ligne", "Espèce", "Type d'erreur"]]

    return data, errors
