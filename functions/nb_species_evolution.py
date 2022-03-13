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

    # Fonction de cumulation des espèces
    def cumulative_species(dataframe: pd.DataFrame) -> pd.DataFrame:
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

    # Données cumulation d'espèces
    all_species_cumulative = cumulative_species(data)
    lr_data = data.loc[data["Menace"] == "Menacé"]
    lr_species_cumulative = cumulative_species(lr_data)
    peuplier_data = data.loc[data["Espèce du substrat"] == "peuplier"]
    peuplier_species_cumulative = cumulative_species(peuplier_data)
    chene_data = data.loc[data["Espèce du substrat"] == "chêne"]
    chene_species_cumulative = cumulative_species(chene_data)
    saule_data = data.loc[data["Espèce du substrat"] == "saule"]
    saule_species_cumulative = cumulative_species(saule_data)
    marronnier_data = data.loc[data["Espèce du substrat"] == "marronnier"]
    marronnier_species_cumulative = cumulative_species(marronnier_data)

    # Création du graphique cumulation d'espèces
    plt.figure()
    plt.plot(all_species_cumulative["Date"], all_species_cumulative["Nb total espèces"], label="Toutes les espèces")
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre total d'espèces")
    plt.ylim(ymin=0)
    plt.plot(lr_species_cumulative["Date"], lr_species_cumulative["Nb total espèces"],
             label="Les espèces de la liste rouge")
    plt.plot(peuplier_species_cumulative["Date"], peuplier_species_cumulative["Nb total espèces"],
             label="Les espèces sur peuplier")
    plt.plot(chene_species_cumulative["Date"], chene_species_cumulative["Nb total espèces"],
             label="Les espèces sur chêne")
    plt.plot(saule_species_cumulative["Date"], saule_species_cumulative["Nb total espèces"],
             label="Les espèces sur saule")
    plt.plot(marronnier_species_cumulative["Date"], marronnier_species_cumulative["Nb total espèces"],
             label="Les espèces sur marronnier")
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois.png", bbox_inches='tight')
    plt.show(block=False)

    # Données cumulation d'espèces liste rouge
    lr_peuplier_data = data.loc[(data["Menace"] == "Menacé") & (data["Espèce du substrat"] == "peuplier")]
    lr_peuplier_data_cumulative = cumulative_species(lr_peuplier_data)
    lr_chene_data = data.loc[(data["Menace"] == "Menacé") & (data["Espèce du substrat"] == "chêne")]
    lr_chene_data_cumulative = cumulative_species(lr_chene_data)
    lr_saule_data = data.loc[(data["Menace"] == "Menacé") & (data["Espèce du substrat"] == "saule")]
    lr_saule_data_cumulative = cumulative_species(lr_saule_data)
    lr_marronnier_data = data.loc[(data["Menace"] == "Menacé") & (data["Espèce du substrat"] == "marronnier")]
    lr_marronnier_data_cumulative = cumulative_species(lr_marronnier_data)

    # Création du graphique cumulation d'espèces liste rouge
    plt.figure()
    plt.plot(lr_species_cumulative["Date"], lr_species_cumulative["Nb total espèces"],
             label="Les espèces de la liste rouge")
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre d'espèces de la liste rouge")
    plt.ylim(ymin=0)
    plt.plot(lr_peuplier_data_cumulative["Date"], lr_peuplier_data_cumulative["Nb total espèces"],
             label="Les espèces du peuplier de la liste rouge")
    plt.plot(lr_chene_data_cumulative["Date"], lr_chene_data_cumulative["Nb total espèces"],
             label="Les espèces du chêne de la liste rouge")
    plt.plot(lr_saule_data_cumulative["Date"], lr_saule_data_cumulative["Nb total espèces"],
             label="Les espèces du saule de la liste rouge")
    plt.plot(lr_marronnier_data_cumulative["Date"], lr_marronnier_data_cumulative["Nb total espèces"],
             label="Les espèces du marronnier de la liste rouge")
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois_lr.png", bbox_inches='tight')
    plt.show(block=False)

    # Données cumulation d'espèces EX, EW, RE, CR, EN, VU total
    exewre_species = data.loc[(data["LR"] == "EX") | (data["LR"] == "EW") | (data["LR"] == "RE")]
    exewre_species_cumulative = cumulative_species(exewre_species)
    cr_species = data.loc[data["LR"] == "CR"]
    cr_species_cumulative = cumulative_species(cr_species)
    en_species = data.loc[data["LR"] == "EN"]
    en_species_cumulative = cumulative_species(en_species)
    vu_species = data.loc[data["LR"] == "VU"]
    vu_species_cumulative = cumulative_species(vu_species)

    # Création du graphique cumulation d'espèces EX, EW, RE, CR, EN, VU total
    plt.figure()
    if len(lr_species_cumulative) > 0:
        plt.plot(lr_species_cumulative["Date"], lr_species_cumulative["Nb total espèces"],
                 label="Les espèces de la liste rouge")
    if len(exewre_species_cumulative) > 0:
        plt.plot(exewre_species_cumulative["Date"], exewre_species_cumulative["Nb total espèces"],
                 label="Les espèces éteintes ou disparues")
    if len(cr_species_cumulative) > 0:
        plt.plot(cr_species_cumulative["Date"], cr_species_cumulative["Nb total espèces"],
                 label="Les espèces en danger critique (CR)")
    if len(en_species_cumulative) > 0:
        plt.plot(en_species_cumulative["Date"], en_species_cumulative["Nb total espèces"],
                 label="Les espèces en danger (EN)")
    if len(vu_species_cumulative) > 0:
        plt.plot(vu_species_cumulative["Date"], vu_species_cumulative["Nb total espèces"],
                 label="Les espèces vulnérables (VU)")
    plt.ylabel("Nombre d'espèces")
    plt.title("Evolution du nombre d'espèces de la liste rouge détaillée")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/especes_cumulees_par_mois_lr_detaillee.png", bbox_inches='tight')
    plt.show(block=False)

    # Nombre d'espèces par mois
    number_species_by_month = data[['Nom', 'Date']].sort_values(by=["Date"])
    number_species_by_month = number_species_by_month.groupby(pd.Grouper(key='Date', freq='1M')).nunique()
    plt.figure()
    plt.bar(number_species_by_month.index, number_species_by_month["Nom"], ec='blue')
    plt.title("Nombre d'espèces par mois")
    plt.ylabel("Nombre d'espèces")
    plt.savefig(directory + "/nbre_especes_par_mois.png", bbox_inches='tight')
    plt.show()

    # Enregistrer le fichier excel
    writer = pd.ExcelWriter(directory + '/donnees.xlsx', engine='xlsxwriter')

    number_species_by_month.to_excel(writer, sheet_name='Nb espèces par mois')

    all_species_cumulative.to_excel(writer, sheet_name='Espèces cumulées', index=False)
    lr_species_cumulative.to_excel(writer, sheet_name='Espèces cumulées LR', index=False)

    peuplier_species_cumulative.to_excel(writer, sheet_name='Espèces du peuplier', index=False)
    chene_species_cumulative.to_excel(writer, sheet_name='Espèces du chêne', index=False)
    saule_species_cumulative.to_excel(writer, sheet_name='Espèces du saule', index=False)
    marronnier_species_cumulative.to_excel(writer, sheet_name='Espèces du marronnier', index=False)

    lr_peuplier_data_cumulative.to_excel(writer, sheet_name='Espèces du peuplier LR', index=False)
    lr_chene_data_cumulative.to_excel(writer, sheet_name='Espèces du chêne LR', index=False)
    lr_saule_data_cumulative.to_excel(writer, sheet_name='Espèces du saule LR', index=False)
    lr_marronnier_data_cumulative.to_excel(writer, sheet_name='Espèces du marronnier LR', index=False)

    exewre_species_cumulative.to_excel(writer, sheet_name='Espèces éteintes ou disparues', index=False)
    cr_species_cumulative.to_excel(writer, sheet_name='Espèces CR', index=False)
    en_species_cumulative.to_excel(writer, sheet_name='Espèces EN', index=False)
    vu_species_cumulative.to_excel(writer, sheet_name='Espèces VU', index=False)
    writer.save()
