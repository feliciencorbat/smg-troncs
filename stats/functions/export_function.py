import os

import numpy as np
import pandas as pd

from stats.functions.export_functions.adjust_columns import adjust_columns
from stats.functions.export_functions.clean_trunks_columns import clean_trunks_columns
from stats.functions.export_functions.lr_errors import lr_errors
from stats.functions.export_functions.new_cf_column import new_cf_column
from stats.functions.export_functions.new_cut_trunks_dataframe import new_cut_trunks_dataframe
from stats.functions.export_functions.new_date_columns import new_date_columns
from stats.functions.export_functions.new_gbif_columns import new_gbif_columns
from stats.functions.export_functions.new_species_column import new_species_column
from stats.functions.export_functions.new_species_dataframe import new_species_dataframe
from stats.functions.export_functions.new_swiss_fungi_count_column import new_swiss_fungi_count_column
from stats.functions.export_functions.new_swiss_fungi_id_column import new_swiss_fungi_id_column
from stats.functions.export_functions.new_swiss_fungi_link_column import new_swiss_fungi_link_column
from stats.functions.export_functions.new_swiss_fungi_lr_column import new_swiss_fungi_lr_column
from stats.functions.export_functions.new_threat_column import new_threat_column
from stats.functions.export_functions.species_errors import species_errors
from stats.functions.export_functions.synonyms_errors import synonyms_errors
from stats.functions.export_functions.test_nb_obs import test_nb_obs
from stats.functions.export_functions.trunks_errors import trunks_errors

"""
Fonction de création d'une liste de données pour les statistiques
"""


def export_function(file) -> None:
    # Création 3 dataframes données, troncs et erreurs
    data = pd.read_excel(file, sheet_name="Observations")
    trunks = pd.read_excel(file, sheet_name="Troncs")
    errors = pd.DataFrame([], )

    # Nombre d'observations au départ
    nb_obs = data.shape[0]

    # Ajouter colonnes mois et saison
    data = new_date_columns(data)

    # Ajouter colonne cf
    data = new_cf_column(data)

    # Ajouter colonne espèce
    data = new_species_column(data)

    # Création du nouveau dataframe species
    print("Création du dataframe species...")
    species = new_species_dataframe(data)

    # Chercher les erreurs dans les noms d'espèces (parenthèses, ...) et les incohérences avec la LR
    print("Recherche des erreurs dans les noms d'espèces (parenthèses, ...)...")
    sp_errors = species_errors(data, species)
    errors = pd.concat([errors, sp_errors])

    # Création colonne menace dans le dataframe species
    species = new_threat_column(species)

    # Création colonnes GBIF dans la dataframe species
    print("Création de la colonne GBIF...")
    species, gbif_errors = new_gbif_columns(species)
    errors = pd.concat([errors, gbif_errors])
    syn_errors = synonyms_errors(species)
    errors = pd.concat([errors, syn_errors])

    # Création colonne SwissFungi Id et SwissFungi Obs dans la dataframe species
    print("Recherche des SwissFungi id...")
    species = new_swiss_fungi_id_column(species)

    # Création colonne SwissFungi Lien dans la dataframe species
    species = new_swiss_fungi_link_column(species)

    # Création colonne SwissFungi LR dans la dataframe species
    print("Recherche des SwissFungi Observations...")
    species = new_swiss_fungi_count_column(species)

    # Création colonne SwissFungi LR dans la dataframe species
    print("Recherche des SwissFungi LR...")
    species = new_swiss_fungi_lr_column(species)

    # Erreurs entre LR et SwissFungi LR
    print("Erreurs en LR et SwissFungi LR...")
    errors_lr = lr_errors(species)
    errors = pd.concat([errors, errors_lr])

    # Joindre le dataframe species au dataframe data
    print("Joindre dataframe species au Dataframe data...")
    data = data.join(species.set_index('Espèce'), on="Espèce", rsuffix='_right')

    # Nettoyer les colonnes liées aux troncs
    print("Nettoyer les colonnes liées aux troncs...")
    trunks, data = clean_trunks_columns(trunks, data)

    # Création du nouveau dataframe de coupe des troncs
    print("Création dataframe coupe des troncs...")
    cut_trunks = new_cut_trunks_dataframe(trunks)

    # Joindre le dataframe coupe des troncs avec troncs
    print("Joindre le dataframe coupe des troncs avec troncs...")
    trunks = trunks.join(cut_trunks.set_index('Identifiant'), on="Identifiant")

    # Joindre le dataframe trunks au dataframe data
    print("Joindre le dataframe troncs au dataframe data...")
    data = data.join(trunks.set_index('Identifiant'), on="Substrat", rsuffix='_right')

    # Ajouter une colonne âge du tronc
    print("Ajouter une colonne âge du tronc...")
    data["Age du tronc"] = (data["Date"] - data["Date de coupe"]) / 365.25

    # Erreurs des troncs
    print("Erreurs des troncs...")
    tru_errors = trunks_errors(data)
    errors = pd.concat([errors, tru_errors])

    # Réarranger les colonnes (ordre, noms, ...)
    print("Réarranger les colonnes (ordre, noms, ...)...")
    data, species, errors = adjust_columns(data, species, errors)

    # Liste des espèces par tronc
    print("Liste des espèces par tronc...")
    trunks_species_serie = data[["Tronc", "Espèce"]].groupby("Tronc")["Espèce"].apply(
        lambda x: list(np.unique(x))).to_frame()
    trunks_species = pd.DataFrame({'Tronc': trunks_species_serie.index, 'Espèces': trunks_species_serie["Espèce"]})
    trunks_species.index.name = None
    trunks_species["Tronc_int"] = trunks_species["Tronc"]
    trunks_species["Tronc_int"] = trunks_species["Tronc_int"].str.replace("G", "", regex=False)
    trunks_species["Tronc_int"] = trunks_species["Tronc_int"].str.replace("D", "", regex=False)
    trunks_species["Tronc_int"] = trunks_species["Tronc_int"].str.replace("_2", "", regex=False)
    trunks_species["Tronc_int"] = pd.to_numeric(trunks_species["Tronc_int"], errors='coerce')
    trunks_species = trunks_species.sort_values('Tronc_int')
    trunks_species = trunks_species[["Tronc", "Espèces"]]

    # Tester si le nombre d'observations est toujours le même
    print("Tester si le nombre d'observations est toujours le même...")
    nb_obs_errors = test_nb_obs(data, nb_obs)
    errors = pd.concat([errors, nb_obs_errors])

    # Enregistrer le fichier excel
    print("Enregistrer le fichier excel...")
    directory = "files/export"
    if not os.path.exists(directory):
        os.makedirs(directory)
    writer = pd.ExcelWriter(directory + '/liste_modifiee.xlsx', engine='xlsxwriter',
                            datetime_format='dd.mm.yyyyy', date_format='dd.mm.yyyyy')

    data.to_excel(writer, sheet_name='Statistiques', index=False)
    for column in data:
        column_length = max(data[column].astype(str).map(len).max(), len(column))
        col_idx = data.columns.get_loc(column)
        writer.sheets['Statistiques'].set_column(col_idx, col_idx, column_length)

    species.to_excel(writer, sheet_name='Espèces', index=False)
    for column in species:
        column_length = max(species[column].astype(str).map(len).max(), len(column))
        col_idx = species.columns.get_loc(column)
        writer.sheets['Espèces'].set_column(col_idx, col_idx, column_length)
        col_idx = species.columns.get_loc('SwissFungi Lien')
        writer.sheets['Espèces'].set_column(col_idx, col_idx, 15)

    trunks.to_excel(writer, sheet_name='Troncs', index=False)
    for column in trunks:
        column_length = max(trunks[column].astype(str).map(len).max(), len(column))
        col_idx = trunks.columns.get_loc(column)
        writer.sheets['Troncs'].set_column(col_idx, col_idx, column_length)

    trunks_species.to_excel(writer, sheet_name='Espèces par tronc', index=False)
    for column in trunks_species:
        column_length = max(trunks_species[column].astype(str).map(len).max(), len(column))
        col_idx = trunks_species.columns.get_loc(column)
        writer.sheets['Espèces par tronc'].set_column(col_idx, col_idx, column_length)

    errors.to_excel(writer, sheet_name='Erreurs', index=False)
    for column in errors:
        column_length = max(errors[column].astype(str).map(len).max(), len(column))
        col_idx = errors.columns.get_loc(column)
        writer.sheets['Erreurs'].set_column(col_idx, col_idx, column_length)
    writer.close()

    print("Exportation terminée")
