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

    writer = pd.ExcelWriter(directory + '/donnees.xlsx', engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Données')

    # Analyse des données
    print("Analyse des données")
    print(rp.summary_cont(data[variable2].groupby(data[variable1])))
    data_excel = pd.DataFrame(rp.summary_cont(data[variable2].groupby(data[variable1])))
    data_excel.to_excel(writer, sheet_name='Analyse des données')
    mods = data[variable1].unique()

    args = []
    for mod in mods:
        args.append(data[variable2][data[variable1] == mod])

    # Validité de l'ANOVA
    anova_validity = True

    # Test de distribution Jarque-Bera
    i = 0
    for arg in args:
        print("\n\nTest de distribution de Jarque-Bera pour la modalité " + mods[i])
        statistic_jarque_bera, p_value_jarque_bera = stats.jarque_bera(arg)
        print("\nP-value de Jarque-Bera est " + str(p_value_jarque_bera))

        i = i + 1

        if p_value_jarque_bera < 0.05:
            print("\nLa distribution ne suit pas une loi normale"
                  "\nLe test ANOVA sera donc caduque.")
            anova_validity = False
        else:
            print("\nLa distribution suit une loi normale.")

    # Test de Levene
    print("\n\nTest de Levene (homogénéité des variances)")
    statistic_levene, p_value_levene = stats.levene(*args, center="mean")
    data_excel = pd.DataFrame({"Statistiques": [statistic_levene], "P-value": [p_value_levene]})
    data_excel.to_excel(writer, sheet_name='Test Levene', index=False)
    print("\nP-value de Levene est " + str(p_value_levene))

    if p_value_levene < 0.05:
        print("\nLes variances des populations ne sont pas homogènes."
              "\nLe test ANOVA sera donc caduque.")
        anova_validity = False
    else:
        print("\nLes variances des populations sont homogènes.")

    # Anova one-way
    print("\n\nTest ANOVA one-way")
    statistic_anova, p_value_anova = stats.f_oneway(*args)
    data_excel = pd.DataFrame({"Statistiques": [statistic_anova], "P-value": [p_value_anova]})
    data_excel.to_excel(writer, sheet_name='Test ANOVA', index=False)
    print("\nP-value de l'ANOVA est " + str(p_value_anova))

    if p_value_anova < 0.05:
        print("\nDonc il y a bien une différence observée entre les moyennes des modalités.")
    else:
        print("\nIl n'y a pas de différence observée entre les moyennes des modalités.")

    if anova_validity:
        print("Les tests de normalité et d'homogénéité des variances rendent le test ANOVA valide.")
    else:
        print("Les tests de normalité et d'homogénéité des variances rendent le test ANOVA non valide."
              "\nNous utilisons alors un test non paramétrique.")

        print("\n\nTest de Kruskal-Wallis")
        statistic_kruskal, p_value_kruskal = stats.kruskal(*args)
        data_excel = pd.DataFrame({"Statistiques": [statistic_kruskal], "P-value": [p_value_kruskal]})
        data_excel.to_excel(writer, sheet_name='Test Kruskal-Wallis', index=False)
        print("\nP-value de Kruskal-Wallis est " + str(p_value_kruskal))

        if p_value_kruskal < 0.05:
            print("\nAu moins un échantillon domine stochastiquement un autre échantillon.")
        else:
            print("\nIl n'y a pas de différences entre les échantillons.")

    writer.save()
