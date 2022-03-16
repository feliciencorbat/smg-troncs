import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats

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

    data = data[[variable1, variable2]]
    data = data.dropna()

    # dossier d'export
    directory = "export/anova " + variable1 + " " + variable2
    if not os.path.exists(directory):
        os.makedirs(directory)

    # graphe boîte à moustaches
    sns.boxplot(x=variable1, y=variable2, data=data)
    plt.title(title)
    plt.savefig(directory + "/boite_moustaches.png", bbox_inches='tight')
    plt.show(block=False)

    # Anova one-way
    mods = data[variable1].unique()

    args = []
    for mod in mods:
        args.append(data[variable2][data[variable1] == mod])

    statistic_anova, p_value_anova = stats.f_oneway(*args)
    print("P-value de l'ANOVA est " + str(p_value_anova))

    if p_value_anova < 0.05:
        print("\nL'hypothèse H0 est rejetée car la p-value est inférieure à 0.05."
              "\nDonc il y a bien une différence observée entre les moyennes des modalités.")
    else:
        print("\nL'hypothèse H0 est acceptée car la p-value est supérieure à 0.05."
              "\nDonc il n'y a pas de différence observée entre les moyennes des modalités.")
