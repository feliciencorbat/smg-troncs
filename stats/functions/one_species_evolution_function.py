import os
import matplotlib
import numpy as np
import pandas as pd
matplotlib.use('agg')
import matplotlib.pyplot as plt


"""
Evolution d'une espèce avec le temps
"""


def one_species_evolution_function(data: pd.DataFrame, species: str, with_cf: bool, location: str, user_id: str) -> None:
    # dossier d'export
    directory = "files/one_species_evolution_" + user_id
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Filtrer espèce
    data = data.loc[data["Espèce"] == species]

    # Filtrer lieu
    if location != "Tous les lieux":
        data = data.loc[data["Lieu"] == location]

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    # Enregistrer le fichier excel
    writer = pd.ExcelWriter(directory + '/one_species_evolution.xlsx', engine='xlsxwriter', datetime_format='dd.mm.yyyyy', date_format='dd.mm.yyyyy')

    # Total observations
    count = data[["Date", "Espèce"]].groupby(pd.Grouper(key='Date', freq='1M')).count()
    total_obs = pd.DataFrame([], )
    total_obs["Obervations"] = count["Espèce"]
    total_obs["Obervations cumulées"] = total_obs.cumsum()
    total_obs.to_excel(writer, sheet_name='Total observations')

    # Création du graphique cumulation dde l'espèce
    plt.figure()
    plt.plot(total_obs.index, total_obs["Obervations cumulées"],
             label="Total observations")

    plt.ylabel("Nombre d'observations")
    plt.title("Evolution du nombre d'observations de " + species)
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/observations_cumulees_par_mois.svg", bbox_inches='tight')
    writer.save()