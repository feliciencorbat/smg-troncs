import os
import numpy as np
import pandas as pd

from functions.export_functions.adjust_columns import adjust_columns
from functions.export_functions.clean_trunks_columns import clean_trunks_columns
from functions.export_functions.new_cf_column import new_cf_column
from functions.export_functions.new_cut_trunks_dataframe import new_cut_trunks_dataframe
from functions.export_functions.new_date_columns import new_date_columns
from functions.export_functions.new_gbif_columns import new_gbif_columns
from functions.export_functions.new_species_column import new_species_column
from functions.export_functions.new_species_dataframe import new_species_dataframe
from functions.export_functions.new_threat_column import new_threat_column
from functions.export_functions.species_errors import species_errors
from functions.export_functions.synonyms_errors import synonyms_errors
from functions.export_functions.trunks_errors import trunks_errors

"""
Fonction de création d'une liste de données pour les statistiques
"""


def export(filename: str) -> None:
    # dossier d'export
    export_directory = "export"
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    # Création 3 dataframes données, troncs et erreurs
    data = pd.read_excel(filename, sheet_name="Observations")
    trunks = pd.read_excel(filename, sheet_name="Troncs")
    errors = pd.DataFrame([], )

    # Ajouter colonnes mois et saison
    data = new_date_columns(data)

    # Ajouter colonne cf
    data = new_cf_column(data)

    # Ajouter colonne espèce
    data = new_species_column(data)

    # Création du nouveau dataframe species
    species = new_species_dataframe(data)

    # Chercher les erreurs dans les noms d'espèces (parenthèses, ...) et les incohérences avec la LR
    sp_errors = species_errors(data, species)
    errors = pd.concat([errors, sp_errors])

    # Création colonne menace dans le dataframe species
    species = new_threat_column(species)

    # Création colonnes GBIF dans la dataframe species
    species, gbif_errors = new_gbif_columns(species)
    errors = pd.concat([errors, gbif_errors])
    syn_errors = synonyms_errors(species)
    errors = pd.concat([errors, syn_errors])

    # Joindre le dataframe species au dataframe data
    data = data.join(species.set_index('Espèce'), on="Espèce", rsuffix='_right')

    # Nettoyer les colonnes liées aux troncs
    trunks, data = clean_trunks_columns(trunks, data)

    # Création du nouveau dataframe de coupe des troncs
    cut_trunks = new_cut_trunks_dataframe(trunks)

    # Joindre le dataframe coupe des troncs avec troncs
    trunks = trunks.join(cut_trunks.set_index('Identifiant'), on="Identifiant")

    # Joindre le dataframe trunks au dataframe data
    data = data.join(trunks.set_index('Identifiant'), on="Substrat", rsuffix='_right')

    # Ajouter une colonne âge du tronc
    data["Age du tronc"] = (data["Date"] - data["Date de coupe"]) / 365.25

    # Erreurs des troncs
    tru_errors = trunks_errors(data)
    errors = pd.concat([errors, tru_errors])

    # Réarranger les colonnes (ordre, noms, ...)
    data, errors = adjust_columns(data, errors)

    # Liste des espèces par tronc
    trunks_species = data[["Tronc", "Espèce"]].groupby("Tronc")["Espèce"].apply(lambda x: list(np.unique(x)))

    # Enregistrer le fichier excel
    writer = pd.ExcelWriter(export_directory + '/liste_modifiee.xlsx', engine='xlsxwriter',
                            datetime_format='dd.mm.yyyyy', date_format='dd.mm.yyyyy')
    data.to_excel(writer, sheet_name='Statistiques', index=False)
    species.to_excel(writer, sheet_name='Espèces', index=False)
    trunks_species.to_excel(writer, sheet_name='Espèces par tronc')
    errors.to_excel(writer, sheet_name='Erreurs', index=False)
    writer.save()
