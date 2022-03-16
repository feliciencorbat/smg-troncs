import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats
import researchpy as rp

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

    # Analyse des données
    print("Analyse des données\n\n")
    print(rp.summary_cont(data[variable2].groupby(data[variable1])))

    mods = data[variable1].unique()

    args = []
    for mod in mods:
        args.append(data[variable2][data[variable1] == mod])

    # Test de Levene
    print("\n\nTest de Levene (égalité des variances)")
    statistic_levene, p_value_levene = stats.levene(*args, center="mean")
    print("\nP-value de Levene est " + str(p_value_levene))

    if p_value_levene < 0.05:
        print("\nLes variances des populations ne sont pas égales."
              "\nLe test ANOVA est donc caduque.")
    else:
        print("\nLes variances des populations sont égales.")

    # Anova one-way
    print("\n\nTest ANOVA one-way")
    statistic_anova, p_value_anova = stats.f_oneway(*args)
    print("\nP-value de l'ANOVA est " + str(p_value_anova))

    if p_value_anova < 0.05:
        print("\nL'hypothèse H0 est rejetée car la p-value est inférieure à 0.05."
              "\nDonc il y a bien une différence observée entre les moyennes des modalités.")
    else:
        print("\nL'hypothèse H0 est acceptée car la p-value est supérieure à 0.05."
              "\nDonc il n'y a pas de différence observée entre les moyennes des modalités.")
