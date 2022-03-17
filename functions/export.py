import json
import os
import urllib.request
import numpy as np
import pandas as pd

"""
Fonction de création d'une liste de données pour les statistiques
"""


def export(filename: str, with_gbif: bool) -> None:
    # dossier d'export
    export_directory = "export"
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    data = pd.read_excel(filename, sheet_name="Observations")
    trunks = pd.read_excel(filename, sheet_name="Troncs")
    error = pd.DataFrame([], )

    """
    Création  colonne saison
    """
    conditions = [
        (data['Date'].dt.month < 3),
        np.logical_and(data['Date'].dt.month == 3, data['Date'].dt.day < 21),
        (data['Date'].dt.month < 6),
        np.logical_and(data['Date'].dt.month == 6, data['Date'].dt.day < 21),
        (data['Date'].dt.month < 9),
        np.logical_and(data['Date'].dt.month == 9, data['Date'].dt.day < 21),
        (data['Date'].dt.month < 12),
        np.logical_and(data['Date'].dt.month == 12, data['Date'].dt.day < 21),
        np.logical_and(data['Date'].dt.month == 12, data['Date'].dt.day >= 21),
    ]
    choices = [
        'Hiver',
        'Hiver',
        'Printemps',
        'Printemps',
        'Eté',
        'Eté',
        'Automne',
        'Automne',
        'Hiver'
    ]
    data["Saison"] = np.select(condlist=conditions, choicelist=choices)

    """
    Ajouter colonne cf.
    """
    data['cf'] = data["Espèce"].str.contains('cf|\?', regex=True)
    data["cf"] = data["cf"].replace(False, "", regex=False)
    data["cf"] = data["cf"].replace(True, "cf.", regex=False)

    """
    Enlever les cf., ? et parenthèses des genres et espèces
    """
    data["Genre"] = data["Genre"].str.replace(r"\(.*?\)", "", regex=True)
    data["Genre"] = data["Genre"].str.replace("cf.", "", regex=False)
    data["Genre"] = data["Genre"].str.replace("cf", "", regex=False)
    data["Genre"] = data["Genre"].str.replace("?", "", regex=False)
    data["Genre"] = data["Genre"].str.strip()

    data["Espèce"] = data["Espèce"].str.replace(r"\(.*?\)", "", regex=True)
    data["Espèce"] = data["Espèce"].str.replace("cf.", "", regex=False)
    data["Espèce"] = data["Espèce"].str.replace("cf", "", regex=False)
    data["Espèce"] = data["Espèce"].str.replace("?", "", regex=False)
    data["Espèce"] = data["Espèce"].str.strip()

    """
    Création colonne Nom binomial
    """
    data["Nom"] = data["Genre"] + " " + data["Espèce"]

    """
    Création du nouveau dataframe species avec 2 colonnes (nom binomial et liste rouge) et tri par ordre alphabétique
    """
    species = data[['Nom', 'LR', 'Fréq']].drop_duplicates()
    species = species.sort_values("Nom")

    """
    Afficher les erreurs dans les noms qui contiennent une parenthèse non fermée ou égal
    """
    errors = data.loc[data["Nom"].str.contains("\)|\(|\=", case=False)]
    errors = errors[["Nom"]]
    errors["Type d'erreur"] = "Erreur de parenthèse non fermée ou de caractère indésirable"
    errors["Ligne"] = errors.index + 2
    error = pd.concat([error, errors])

    """
    Chercher les incohérences entre Nom et LR
    """
    size = species.groupby(['Nom']).size()
    errors = size[size >= 2].index
    for err in errors:
        print(err + " a une incohérence avec la liste rouge")
        error_row = pd.DataFrame({'Nom': [err],
                                  "Type d'erreur": ["Il y a une incohérence entre l'espèce et la liste rouge"]})
        error = pd.concat([error, error_row])

    """
    Création colonne Menace
    """
    conditions = [
        (species['Fréq'] == 'R'),
        (species['LR'] == 'EX'),
        (species['LR'] == 'EW'),
        (species['LR'] == 'RE'),
        (species['LR'] == 'CR'),
        (species['LR'] == 'EN'),
        (species['LR'] == 'VU'),
        (species['LR'] == 'LC'),
        (species['LR'] == 'NT')
    ]
    choices = [
        'Menacé',
        'Eteint',
        'Eteint',
        'Eteint',
        'Menacé',
        'Menacé',
        'Menacé',
        'Non menacé',
        'Non menacé'
    ]
    species["Menace"] = np.select(condlist=conditions, choicelist=choices, default='Menace inconnue')

    """
    Création colonne Mois
    """
    data['Mois'] = data['Date'].dt.month

    """
    Création colonnes GBIF
    """
    if with_gbif:
        species["Nom actuel"] = None
        species["Phylum"] = None
        species["Ordre"] = None
        for row in species.itertuples():
            try:
                name_url = urllib.parse.quote(row.Nom)
                response = urllib.request.urlopen(
                    "https://api.gbif.org/v1/species/match?kingdom=Fungi&name=" + name_url)

                json_data = response.read().decode("utf-8", "replace")
                gbif_match = json.loads(json_data)
                if gbif_match["rank"] == "SPECIES" or gbif_match["rank"] == "VARIETY" \
                        or gbif_match["rank"] == "SUBSPECIES" or gbif_match["rank"] == "FORM":

                    species.at[row.Index, "Nom actuel"] = gbif_match["canonicalName"]
                    if "phylum" in gbif_match:
                        species.at[row.Index, "Phylum"] = gbif_match["phylum"]

                    if "order" in gbif_match:
                        species.at[row.Index, "Ordre"] = gbif_match["order"]

                    if "acceptedUsageKey" in gbif_match:
                        accepted_key = gbif_match["acceptedUsageKey"]

                        try:
                            response = urllib.request.urlopen(
                                "https://api.gbif.org/v1/species/" + str(accepted_key))

                            json_data = response.read().decode("utf-8", "replace")
                            gbif_species = json.loads(json_data)

                            species.at[row.Index, "Nom actuel"] = gbif_species["canonicalName"]
                            if "phylum" in gbif_match:
                                species.at[row.Index, "Phylum"] = gbif_species["phylum"]

                            if "order" in gbif_match:
                                species.at[row.Index, "Ordre"] = gbif_species["order"]

                            print("Nouveau nom: " + gbif_species["canonicalName"])

                        except:
                            print("Erreur de communication avec GBIF")

                else:
                    print(row.Nom + " non récupérée par GBIF")
                    error_row = pd.DataFrame({'Ligne': [row.Index + 2], 'Nom': [row.Nom],
                                              "Type d'erreur": ["L'espèce n'a pas été trouvée par GBIF"]})
                    error = pd.concat([error, error_row], ignore_index=True, axis=0)
            except:
                print("Erreur de communication avec GBIF")
            finally:
                print(row.Nom)

        """
        Chercher les synonymes
        """
        species_synonyms = species[['Nom', 'Nom actuel']].drop_duplicates()
        size = species_synonyms.groupby(['Nom actuel']).size()

        errors = size[size >= 2].index
        for err in errors:
            print(err + " a une synonymie")
            error_row = pd.DataFrame({'Nom': [err],
                                      "Type d'erreur": ["Il y a une synonymie détectée par GBIF"]})
            error = pd.concat([error, error_row])

    # Joindre le dataframe species au dataframe data
    data = data.join(species.set_index('Nom'), on="Nom", rsuffix='_right')

    """
    Gestion des troncs
    """
    # Enlever les parenthèses des troncs et supprimer certaines colonnes
    trunks["Identifiant"] = trunks["Identifiant"].str.replace(r"\(.*?\)", "", regex=True)
    trunks["Identifiant"] = trunks["Identifiant"].str.strip()

    # Ajouter une colonne âge du tronc moyen
    trunks["Coupé entre"] = trunks["Coupé entre"].str.replace("?", "", regex=False)
    trunks["Coupé entre"] = trunks["Coupé entre"].str.replace("-", "", regex=False)
    trunks["Coupé entre"] = trunks["Coupé entre"].str.replace("hiver", "", regex=False)
    trunks["Coupé entre"] = trunks["Coupé entre"].str.replace("Hiver", "", regex=False)
    trunks["Coupé entre"] = trunks["Coupé entre"].str.replace(" ", "", regex=False)
    trunks["Coupé début"] = pd.to_datetime(((trunks["Coupé entre"].str[:4]) + "0101").astype(int), format='%Y%m%d')
    trunks["Coupé fin"] = pd.to_datetime(((trunks["Coupé entre"].str[-4:]) + "1231").astype(int), format='%Y%m%d')
    trunks["Coupé moyen"] = trunks["Coupé début"] + ((trunks["Coupé fin"] - trunks["Coupé début"]) / 2)

    # Joindre le dataframe trunks au dataframe data
    data["Substrat"] = data["Substrat"].str.replace("tronc ", "", regex=False)
    data = data.join(trunks.set_index('Identifiant'), on="Substrat", rsuffix='_right')

    # Ajouter une colonne âge du tronc
    data["Age tronc"] = (data["Date"] - data["Coupé moyen"]) / 365.25

    # Erreurs: Espèce du substrat absente
    errors = data[data['Espèce du substrat_right'].isnull()]
    errors = errors[['Nom']]
    errors["Type d'erreur"] = "Absence de l'espèce du substrat (tronc absent dans la feuille Troncs)"
    errors["Ligne"] = errors.index + 2
    error = pd.concat([error, errors])

    # Erreurs: Incohérence dans l'espèce du substrat
    errors = data[(data['Espèce du substrat'] != data['Espèce du substrat_right'])
                  & data['Espèce du substrat_right'].notnull()]
    errors = errors[['Nom']]
    errors["Type d'erreur"] = "Incohérence dans l'espèce du substrat"
    errors["Ligne"] = errors.index + 2
    error = pd.concat([error, errors])

    # Colonne date de type datetime en type date
    data["Date"] = pd.to_datetime(data['Date']).dt.date

    # Bien typer et garder uniquement les colonnes nécessaires
    if with_gbif:
        data = data[["Date", "Saison", "Mois", "Nom", "Nom actuel", "Phylum", "Ordre", "cf", "LR", "Menace", "Substrat",
                     "Espèce du substrat",
                     "D. moyen", "Longueur", "Pourriture", "Lieu", "Groupe troncs", "Age tronc"]]
    else:
        data = data[["Date", "Saison", "Mois", "Nom", "cf", "LR", "Menace", "Substrat", "Espèce du substrat", "D. moyen",
                     "Longueur", "Pourriture", "Lieu", "Groupe troncs", "Age tronc"]]
    error = error[["Ligne", "Nom", "Type d'erreur"]]

    # Liste des espèces par tronc
    trunks_species = data[["Substrat", "Nom"]].groupby("Substrat")["Nom"].apply(lambda x: list(np.unique(x)))

    # Enregistrer le fichier excel
    writer = pd.ExcelWriter(export_directory + '/liste_modifiee.xlsx', engine='xlsxwriter',
                            datetime_format='dd.mm.yyyyy', date_format='dd.mm.yyyyy')
    data.to_excel(writer, sheet_name='Statistiques', index=False)
    species.to_excel(writer, sheet_name='Espèces', index=False)
    trunks_species.to_excel(writer, sheet_name='Espèces par tronc')
    error.to_excel(writer, sheet_name='Erreurs', index=False)
    writer.save()
