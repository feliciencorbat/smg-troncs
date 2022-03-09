import os
import pandas as pd
from matplotlib import pyplot as plt

"""
Fonction de distribution d'une variable et création d'un graphe en tuyaux d'orgue
"""


def distribution_bar(data: pd.DataFrame, filename: str, variable: str, limit: int = 0) -> None:
    print("\nDistribution de la variable " + variable + "\n")

    # Gestion de la limite
    if limit == 0:
        data[variable].value_counts(normalize=False).plot(kind='bar')
    else:
        data[variable].value_counts(normalize=False)[:limit].plot(kind='bar')

    # dossier d'export
    dirname = os.path.dirname(filename)
    directory = dirname + "/distribution " + variable
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(directory + "/bar.svg", bbox_inches='tight')
    plt.savefig(directory + "/bar.png", bbox_inches='tight')

    plt.show()
