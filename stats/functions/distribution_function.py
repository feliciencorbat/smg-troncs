import os
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""
Fonction de distribution d'une variable et création d'un graphe en tuyaux d'orgue
"""


def distribution_function(data: pd.DataFrame, variable: str, title: str, limit: int, with_cf: bool,
                          location: str) -> None:
    print("\nDistribution de la variable " + variable + "\n")

    # Filtrer lieu
    if location != "Tous les lieux":
        data = data.loc[data["Lieu"] == location]

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    # Gestion de la limite
    if limit == 0:
        data = data[variable].value_counts(normalize=False)
    else:
        data = data[variable].value_counts(normalize=False)[:limit]

    # dossier files/distribution
    directory = "stats/static/distribution"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # export excel
    data.to_excel(directory + "/distribution.xlsx")

    # Graphe tuyaux d'orgue
    plt.figure()
    plt.bar(data.index, data.values)
    plt.ylabel("Nombre d'observations")
    plt.xticks(rotation=90)
    plt.title(title)
    plt.savefig(directory + "/bars.png", bbox_inches='tight')

    # Graphe camembert
    plt.figure()
    plt.pie(data, labels=data.index)
    plt.title(title)
    plt.savefig(directory + "/pie.png", bbox_inches='tight')
