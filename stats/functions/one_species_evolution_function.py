import datetime
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

    year = data.iloc[-1]["Date"].year
    month = data.iloc[-1]["Date"].month
    last_date = datetime.datetime(year=year, month=month, day=28)


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

    # Création du graphique cumulation de l'espèce
    total_obs = cumulative_observations(data, last_date)
    total_obs.to_excel(writer, sheet_name='Toutes les observations')
    plt.figure()
    plt.plot(total_obs.index, total_obs["Observations cumulées"],
             label="Observations totales")

    plt.ylabel("Nombre d'observations")
    plt.title("Evolution du nombre d'observations de " + species)
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/observations_cumulees_par_mois.svg", bbox_inches='tight')

    # Observations par troncs
    plt.figure()
    for trunk in data["Tronc"].dropna().unique():
        trunk_obs = data.loc[(data["Tronc"] == trunk)]
        trunk_obs = cumulative_observations(trunk_obs, last_date)
        if len(trunk_obs) > 0:
            plt.plot(trunk_obs.index, trunk_obs["Observations cumulées"],
                     label="Tronc " + str(trunk))
            trunk_obs.to_excel(writer, sheet_name="Observations sur tronc " + trunk)

    plt.ylabel("Nombre d'observations")
    plt.title("Evolution du nombre d'observations de " + species + " sur troncs")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/observations_cumulees_par_mois_troncs.svg", bbox_inches='tight')

    # Observations par groupes troncs
    plt.figure()
    for trunk_group in data["Groupe troncs"].dropna().unique():
        trunk_group_obs = data.loc[(data["Groupe troncs"] == trunk_group)]
        trunk_group_obs = cumulative_observations(trunk_group_obs, last_date)
        if len(trunk_group_obs) > 0:
            plt.plot(trunk_group_obs.index, trunk_group_obs["Observations cumulées"],
                     label="Groupe de troncs " + str(trunk_group))
            trunk_group_obs.to_excel(writer, sheet_name="Observations groupe tronc " + trunk_group)

    plt.ylabel("Nombre d'observations")
    plt.title("Evolution du nombre d'observations de " + species + " sur groupes de troncs")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/observations_cumulees_par_mois_groupe_troncs.svg", bbox_inches='tight')

    # Observations par espèces de troncs
    plt.figure()
    for trunk_species in data["Espèce du tronc"].dropna().unique():
        trunk_species_obs = data.loc[(data["Espèce du tronc"] == trunk_species)]
        trunk_species_obs = cumulative_observations(trunk_species_obs, last_date)
        if len(trunk_species_obs) > 0:
            plt.plot(trunk_species_obs.index, trunk_species_obs["Observations cumulées"],
                     label=str(trunk_species))
            trunk_species_obs.to_excel(writer, sheet_name="Observations sur " + trunk_species)

    plt.ylabel("Nombre d'observations")
    plt.title("Evolution du nombre d'observations de " + species + " sur espèces de troncs")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/observations_cumulees_par_mois_especes_troncs.svg", bbox_inches='tight')

def cumulative_observations(data: pd.DataFrame, last_date) -> pd.DataFrame:
    count = data[["Date", "Espèce"]].groupby(pd.Grouper(key='Date', freq='1M')).count()
    observations = pd.DataFrame([], )
    observations["Observations"] = count["Espèce"]
    observations["Observations cumulées"] = observations.cumsum()
    observations_last_date = observations.iloc[-1].name


    # Ajouter une ligne de la dernière date du dataframe total si absente
    if len(observations) > 0:
        if observations_last_date < last_date:
            new_row = observations.iloc[-1:]
            new_row = new_row.rename(index={observations_last_date: last_date})
            new_row['Observations'] = 0
            observations = pd.concat([observations, new_row])

    return observations