import os
import pandas as pd
from matplotlib import pyplot as plt

"""
Evolution du nombre d'espèces avec le temps
"""


def nb_species_evolution(filename: str) -> None:
    # dossier d'export
    dirname = os.path.dirname(filename)
    directory = dirname + "/Evolution especes"
    if not os.path.exists(directory):
        os.makedirs(directory)

    data = pd.read_excel(filename, sheet_name="Sheet1")

    # Fonction de cumulation des espèces
    def cumulative_species(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe[['Nom', 'Date']].sort_values(by=["Date"])
        prov_cumulative_species = dataframe.groupby(pd.Grouper(key='Date', freq='1M'))["Nom"].apply(list)
        cumulative_species_data = pd.DataFrame(columns=['Date', 'Nouvelles espèces', 'Total espèces'])
        i = int(0)
        for index, value in prov_cumulative_species.items():
            if i == 0:
                temporary_row = pd.DataFrame({'Date': [index], 'Nouvelles espèces': [value], 'Total espèces': [value]})
                cumulative_species_data = pd.concat([cumulative_species_data, temporary_row])
            else:
                new_species = []
                for species in value:
                    if species not in cumulative_species_data.iloc[-1, cumulative_species_data.columns.get_loc("Total "
                                                                                                               "espèces")]:
                        if species not in new_species:
                            new_species.append(species)

                old_species = cumulative_species_data.iloc[-1, cumulative_species_data.columns.get_loc("Total espèces")]+new_species
                temporary_row = pd.DataFrame(
                    {'Date': [index], 'Nouvelles espèces': [new_species], 'Total espèces': [old_species]})
                cumulative_species_data = pd.concat([cumulative_species_data, temporary_row])
            i = int(i) + 1

        cumulative_species_data["Nb nouvelles espèces"] = cumulative_species_data['Nouvelles espèces'].apply(
            lambda x: len(x))
        cumulative_species_data["Nb total espèces"] = cumulative_species_data['Total espèces'].apply(lambda x: len(x))
        return cumulative_species_data

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

    # Enregistrement fichier excel
    all_species_cumulative.to_excel(directory + "/especes_cumulees_par_mois.xlsx")
    lr_species_cumulative.to_excel(directory + "/especes_lr_cumulees_par_mois.xlsx")

    # Création du graphique
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

    # Nombre d'espèces par mois
    number_species_by_month = data[['Nom', 'Date']].sort_values(by=["Date"])
    number_species_by_month = number_species_by_month.groupby(pd.Grouper(key='Date', freq='1M')).nunique()
    number_species_by_month.to_excel(directory + "/nbre_especes_par_mois.xlsx")
    plt.figure()
    plt.bar(number_species_by_month.index, number_species_by_month["Nom"], ec='blue')
    plt.title("Nombre d'espèces par mois")
    plt.ylabel("Nombre d'espèces")
    plt.savefig(directory + "/nbre_especes_par_mois.png", bbox_inches='tight')
    plt.show()
