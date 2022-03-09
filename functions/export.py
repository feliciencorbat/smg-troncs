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
    dirname = os.path.dirname(filename)
    export_directory = dirname + "/export"
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    data = pd.read_excel(filename, sheet_name="Observations")
    trunks = pd.read_excel(filename, sheet_name="Troncs")
    error = pd.DataFrame([], )

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
    Suppression de certaines colonnes
    """
    data = data.drop(columns=['Genre', 'Espèce', 'Zone/Lieu', 'Auteurs', 'Abondance', 'X', 'Y', 'Canton', 'Alt',
                              'Végétation', 'Photo', 'B/A/M', 'm/nm/i', 'Legit', 'Dét', 'Exsiccata',
                              'Réf Litt Déter'])

    """
    Création du nouveau dataframe species avec 2 colonnes (nom binomial et liste rouge) et tri par ordre alphabétique
    """
    species = data[['Nom', 'LR', 'Fréq']].drop_duplicates()
    species = species.sort_values("Nom")

    """
    Afficher les erreurs dans les noms qui contiennent une parenthèse non fermée ou égal
    """
    errors = data.loc[data["Nom"].str.contains("\)|\(|\=", case=False)]
    errors = errors.drop(columns=['Substrat', 'Espèce du substrat', 'Date', 'LR'])
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
    Suppression de certaines colonnes
    """
    data = data.drop(columns=['LR', 'Fréq'])

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
        species = species.drop(columns=['LR', 'Phylum', 'Ordre', 'Menace'])
        species = species[['Nom', 'Nom actuel']].drop_duplicates()
        size = species.groupby(['Nom actuel']).size()

        errors = size[size >= 2].index
        for err in errors:
            print(err + " a une synonymie")
            error_row = pd.DataFrame({'Nom': [err],
                                      "Type d'erreur": ["Il y a une synonymie détectée par GBIF"]})
            error = pd.concat([error, error_row])

    # Joindre le dataframe species au dataframe data
    data = data.join(species.set_index('Nom'), on="Nom", lsuffix='_left', rsuffix='_right')

    """
    Gestion des troncs
    """
    # Enlever les parenthèses des troncs et supprimer certaines colonnes
    trunks["Identifiant"] = trunks["Identifiant"].str.replace(r"\(.*?\)", "", regex=True)
    trunks["Identifiant"] = trunks["Identifiant"].str.strip()
    trunks["Coupé entre"] = trunks["Coupé entre"].str.replace("?", "", regex=False)
    trunks = trunks.drop(columns=['Diamètres', 'Rem.', 'Pourriture'])

    # Joindre le dataframe trunks au dataframe data
    data["Substrat"] = data["Substrat"].str.replace("tronc ", "", regex=False)
    data = data.join(trunks.set_index('Identifiant'), on="Substrat", rsuffix='_right')
    data = data.sort_index()

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

    # Liste des espèces par tronc
    trunks_species = data[["Substrat", "Nom"]].groupby("Substrat")["Nom"].apply(lambda x: list(np.unique(x)))

    species.to_excel(export_directory + "/liste_modifiee_especes.xlsx", index=False)
    trunks_species.to_excel(export_directory + "/liste_especes_par_tronc.xlsx")
    error.to_excel(export_directory + "/liste_modifiee_erreurs.xlsx", index=False)
    data.to_excel(export_directory + "/liste_modifiee.xlsx", index=False)
