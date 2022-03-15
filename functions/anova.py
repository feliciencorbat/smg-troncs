import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

"""
Fonction ANOVA entre variable qualitative et quantitative
"""


def anova_test(data: pd.DataFrame, variable1: str, variable2: str, title: str,
               with_cf: bool, location: str) -> None:
    # Filtrer lieu
    if location != "Tous les lieux":
        data = data.loc[data["Lieu"] == location]

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    print("\nTest ANOVA pour les variables " + variable1 + " et " + variable2 + "\n")

    # dossier d'export
    directory = "export/anova " + variable1 + " " + variable2
    if not os.path.exists(directory):
        os.makedirs(directory)

    sns.boxplot(x=variable1, y=variable2, data=data)
    plt.title(title)
    plt.savefig(directory + "/boite_moustaches.png", bbox_inches='tight')
    plt.show(block=False)