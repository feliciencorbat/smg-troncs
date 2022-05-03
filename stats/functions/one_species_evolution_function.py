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

    # Création du graphique cumulation de l'espèce
    total_obs = cumulative_observations(data)
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
        trunk_obs = cumulative_observations(trunk_obs)
        if trunk_obs.iloc[-1]["Observations cumulées"] > 0:
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
        trunk_group_obs = cumulative_observations(trunk_group_obs)
        if trunk_group_obs.iloc[-1]["Observations cumulées"] > 0:
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
        trunk_species_obs = cumulative_observations(trunk_species_obs)
        if trunk_species_obs.iloc[-1]["Observations cumulées"] > 0:
            plt.plot(trunk_species_obs.index, trunk_species_obs["Observations cumulées"],
                     label="Sur " + str(trunk_species))
            trunk_species_obs.to_excel(writer, sheet_name="Observations sur " + trunk_species)

    plt.ylabel("Nombre d'observations")
    plt.title("Evolution du nombre d'observations de " + species + " sur espèces de troncs")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.savefig(directory + "/observations_cumulees_par_mois_especes_troncs.svg", bbox_inches='tight')

    writer.save()

def cumulative_observations(data: pd.DataFrame) -> pd.DataFrame:
    count = data[["Date", "Espèce"]].groupby(pd.Grouper(key='Date', freq='1M')).count()
    observations = pd.DataFrame([], )
    observations["Obervations"] = count["Espèce"]
    observations["Observations cumulées"] = observations.cumsum()
    return observations