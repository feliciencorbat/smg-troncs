from typing import Tuple

import pandas as pd


def adjust_columns(data: pd.DataFrame, species: pd.DataFrame, errors: pd.DataFrame) -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Colonne date de type datetime en type date
    data["Date"] = pd.to_datetime(data['Date']).dt.date

    # Renommer les colonnes de data
    data = data.rename(columns={"LR": "Liste rouge", "Substrat": "Tronc", "Espèce du substrat": "Espèce du tronc",
                                "D. moyen": "Diamètre moyen", "Pourriture": "Degré de pourriture", "Fréq": "Fréquence"})

    # Garder uniquement les colonnes nécessaires
    data = data[
        ["Date", "Année", "Saison", "Mois", "Espèce", "Auteur", "Espèce actuelle", "Auteur actuel", "Phylum", "Ordre", "cf", "Liste rouge", "Menace", "Fréquence",
         "Tronc", "Espèce du tronc", "Diamètre moyen", "Longueur", "Degré de pourriture", "Lieu", "Groupe troncs",
         "Date de coupe", "Age du tronc"]]

    # Renommer les colonnes de species
    species = species.rename(columns={"LR": "Liste rouge", "Fréq": "Fréquence"})

    # Garder uniquement les colonnes nécessaires
    species = species[
        ["Espèce", "Auteur", "SwissFungi Lien", "Espèce actuelle", "Auteur actuel", "SwissFungi Observations", "Liste rouge", "SwissFungi LR",
         "Fréquence", "Menace", "SwissFungi"]]

    errors = errors[["Ligne", "Espèce", "Type d'erreur"]]

    return data, species, errors
