from typing import Tuple

import pandas as pd


def adjust_columns(data: pd.DataFrame, species: pd.DataFrame, errors: pd.DataFrame) -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Colonne date de type datetime en type date
    data["Date"] = pd.to_datetime(data['Date']).dt.date

    # Renommer les colonnes de data
    data = data.rename(columns={"LR": "Liste rouge", "Substrat": "Tronc", "Espèce du substrat": "Espèce du tronc",
                                "D. moyen": "Diamètre moyen", "Pourriture": "Degré de pourriture"})

    # Garder uniquement les colonnes nécessaires
    data = data[
        ["Date", "Saison", "Mois", "Espèce", "Espèce actuelle", "Phylum", "Ordre", "cf", "Liste rouge", "Menace",
         "Tronc", "Espèce du tronc", "Diamètre moyen", "Longueur", "Degré de pourriture", "Lieu", "Groupe troncs",
         "Date de coupe", "Age du tronc"]]

    # Renommer les colonnes de species
    species = species.rename(columns={"LR": "Liste rouge", "Fréq": "Fréquence"})

    # Garder uniquement les colonnes nécessaires
    species = species[
        ["Espèce", "SwissFungi Lien", "Espèce actuelle", "SwissFungi Observations", "Liste rouge", "SwissFungi LR", "Fréquence",
         "Menace"]]

    errors = errors[["Ligne", "Espèce", "Type d'erreur"]]

    return data, species, errors
