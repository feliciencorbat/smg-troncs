import os
import pandas as pd
from matplotlib import pyplot as plt

"""
Fonction de distribution d'une variable et création d'un graphe en tuyaux d'orgue
"""


def distribution_bar(data: pd.DataFrame, variable: str, title: str, limit: int, with_cf: bool) -> None:
    print("\nDistribution de la variable " + variable + "\n")

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    # Gestion de la limite
    if limit == 0:
        data = data[variable].value_counts(normalize=False)
    else:
        data = data[variable].value_counts(normalize=False)[:limit]

    # dossier d'export
    directory = "export/distribution " + variable
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.figure()
    plt.bar(data.index, data.values)
    plt.ylabel("Nombre d'observations")
    plt.xticks(rotation=90)
    plt.title(title)
    plt.savefig(directory + "/" + variable + "_" + str(limit) + ".png", bbox_inches='tight')
    plt.show()
    data.to_excel(directory + "/" + variable + "_" + str(limit) + ".xlsx")
