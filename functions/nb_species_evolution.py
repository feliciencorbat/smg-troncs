import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

"""
Evolution du nombre d'espèces avec le temps
"""


def nb_species_evolution(data: pd.DataFrame, with_cf: bool, location: str) -> None:
    # dossier d'export
    directory = "export/Evolution especes"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Filtrer lieu
    if location != "Tous les lieux":
        data = data.loc[data["Lieu"] == location]

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    # Enregistrer le fichier excel
    writer = pd.ExcelWriter(directory + '/donnees.xlsx', engine='xlsxwriter',
                            datetime_format='dd.mm.yyyyy', date_format='dd.mm.yyyyy')

    # Données cumulation d'espèces
    all_species_cumulative = cumulative_species(data, data)
    lr_data = data.loc[data["Menace"] == "Menacé"]
    lr_species_cumulative = cumulative_species(lr_data, data)

    all_species_cumulative.to_excel(writer, sheet_name='Espèces cumulées', index=False)
    lr_species_cumulative.to_excel(writer, sheet_name='Espèces cumulées LR', index=False)

    # Création du graphique cumulation d'espèces
    plt.figure()
    plt.plot(all_species_cumulative["Date"], all_species_cumulative["Nb total espèces"], label="Toutes les espèces")
    for tree in data["Espèce du substrat"].dropna().unique():
        tree_species = data.loc[(data["Espèce du substrat"] == tree)]
        tree_species_cumulative = cumulative_species(tree_species, data)
        plt.plot(tree_species_cumulative["Date"], tree_species_cumulative["Nb total espèces"],
                 label="Les espèces sur " + str(tree))
        tree_species_cumulative.to_excel(writer, sheet_name="Espèces sur " + tree.replace("?", "inconnu"),
                                         index=False)
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre total d'espèces")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois.png", bbox_inches='tight')
    plt.show(block=False)

    # Création du graphique cumulation d'espèces liste rouge par arbres
    plt.figure()
    plt.plot(lr_species_cumulative["Date"], lr_species_cumulative["Nb total espèces"],
             label="Les espèces de la liste rouge")
    for tree in data["Espèce du substrat"].dropna().unique():
        tree_lr_species = data.loc[(data["Espèce du substrat"] == tree) & (data["Menace"] == "Menacé")]
        tree_lr_species_cumulative = cumulative_species(tree_lr_species, data)
        plt.plot(tree_lr_species_cumulative["Date"], tree_lr_species_cumulative["Nb total espèces"],
                 label="Les espèces de la liste rouge sur " + str(tree))
        tree_lr_species_cumulative.to_excel(writer, sheet_name="Espèces LR sur " +
                                                               tree.replace("?", "inconnu"), index=False)
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre d'espèces de la liste rouge")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois_lr.png", bbox_inches='tight')
    plt.show(block=False)

    # Création du graphique cumulation d'espèces EX, EW, RE, CR, EN, VU total
    plt.figure()
    if len(lr_species_cumulative) > 0:
        plt.plot(lr_species_cumulative["Date"], lr_species_cumulative["Nb total espèces"],
                 label="Les espèces de la liste rouge")
    for lr in data["LR"].dropna().unique():
        if lr != "LC":
            lr_group_species = data.loc[data["LR"] == lr]
            lr_group_species_cumulative = cumulative_species(lr_group_species, data)
            plt.plot(lr_group_species_cumulative["Date"], lr_group_species_cumulative["Nb total espèces"],
                     label="Les espèces de la liste rouge " + str(lr))
            lr_group_species_cumulative.to_excel(writer, sheet_name='Espèces ' + str(lr), index=False)
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre d'espèces de la liste rouge détaillée")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois_lr_detaillee.png", bbox_inches='tight')
    plt.show(block=False)

    # Création du graphique cumulation d'espèces selon groupe de troncs
    plt.figure()
    for tree_group in data["Groupe troncs"].dropna().unique():
        tree_group_species = data.loc[data["Groupe troncs"] == tree_group]
        tree_group_species_cumulative = cumulative_species(tree_group_species, data)
        plt.plot(tree_group_species_cumulative["Date"], tree_group_species_cumulative["Nb total espèces"],
                 label="Les espèces du groupe de troncs " + str(tree_group))
        tree_group_species_cumulative.to_excel(writer, sheet_name="Espèces par troncs " + str(tree_group),
                                               index=False)
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre d'espèces des groupes de troncs")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois_groupe_troncs.png", bbox_inches='tight')
    plt.show(block=False)

    # Nombre d'espèces par mois
    number_species_by_month = data[['Nom', 'Date']].sort_values(by=["Date"])
    number_species_by_month = number_species_by_month.groupby(pd.Grouper(key='Date', freq='1M')).nunique()
    plt.figure()
    plt.bar(number_species_by_month.index, number_species_by_month["Nom"], ec='blue')
    plt.title("Nombre d'espèces par mois")
    plt.ylabel("Nombre d'espèces")
    plt.savefig(directory + "/nbre_especes_par_mois.png", bbox_inches='tight')
    plt.show(block=False)

    number_species_by_month.to_excel(writer, sheet_name='Nb espèces par mois')
    writer.save()


# Fonction de cumulation des espèces
def cumulative_species(dataframe: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe[['Nom', 'Date']].sort_values(by=["Date"])
    prov_cumulative_species = dataframe.groupby(pd.Grouper(key='Date', freq='1M'))["Nom"].apply(
        lambda x: list(np.unique(x)))
    cumulative_species_data = pd.DataFrame(columns=['Date', 'Nouvelles espèces', 'Total espèces'])
    i = int(0)
    for index, value in prov_cumulative_species.items():
        if i == 0:
            temporary_row = pd.DataFrame({'Date': [index], 'Nouvelles espèces': [value], 'Total espèces': [value]})
            cumulative_species_data = pd.concat([cumulative_species_data, temporary_row])
        else:
            new_species = []
            for species in value:
                if species not in \
                        cumulative_species_data.iloc[-1, cumulative_species_data.columns.get_loc("Total espèces")]:
                    new_species.append(species)

            old_species = cumulative_species_data.iloc[
                              -1, cumulative_species_data.columns.get_loc("Total espèces")] + new_species
            temporary_row = pd.DataFrame(
                {'Date': [index], 'Nouvelles espèces': [new_species], 'Total espèces': [old_species]})
            cumulative_species_data = pd.concat([cumulative_species_data, temporary_row])
        i = int(i) + 1

    # Ajouter une ligne de la dernière date du dataframe total si absente
    if len(cumulative_species_data) > 0:
        if cumulative_species_data.iloc[-1]["Date"] < data.iloc[-1]["Date"]:
            new_row = cumulative_species_data.iloc[-1:]
            new_row.at[0, 'Date'] = data.iloc[-1]["Date"]
            new_row.at[0, 'Nouvelles espèces'] = []
            cumulative_species_data = pd.concat([cumulative_species_data, new_row])

    # Comptage des espèces
    cumulative_species_data["Nb nouvelles espèces"] = cumulative_species_data['Nouvelles espèces'].apply(
        lambda x: len(x))
    cumulative_species_data["Nb total espèces"] = cumulative_species_data['Total espèces'].apply(lambda x: len(x))
    return cumulative_species_data
