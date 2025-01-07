import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import researchpy as rp

"""
Fonction ANOVA entre variable qualitative et quantitative
"""


def anova_function(data: pd.DataFrame, variable1: str, variable2: str, title: str,
                   with_cf: bool, location: str, minimum: int, user_id: str):
    # Filtrer lieu
    if location != "Tous les lieux":
        data = data.loc[data["Lieu"] == location]

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    data = data[[variable1, variable2]]
    data = data.dropna()

    # Minimum d'occurences par modalité
    if minimum < 3:
        minimum = 3

    variables_size = data.groupby([variable1]).size()
    print(variables_size)
    for index, value in variables_size.items():
        if value < minimum:
            data = data.loc[data[variable1] != index]

    # dossier d'export
    directory = "files/anova_" + user_id
    if not os.path.exists(directory):
        os.makedirs(directory)

    # graphe boîte à moustaches
    plt.figure()
    sns.boxplot(x=variable1, y=variable2, data=data)
    plt.title(title)
    plt.savefig(directory + "/boite_moustaches.svg", bbox_inches='tight')

    writer = pd.ExcelWriter(directory + '/anova.xlsx', engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Données')

    # Analyse des données
    analyzed_data = rp.summary_cont(data[variable2].groupby(data[variable1]))
    data_excel = pd.DataFrame(analyzed_data)
    data_excel.to_excel(writer, sheet_name='Analyse des données')
    mods = data[variable1].unique()

    args = []
    for mod in mods:
        args.append(data[variable2][data[variable1] == mod])

    # Validité de l'ANOVA
    anova_validity = True

    # Test de normalité de Shapiro-Wilk
    i = 0
    shapiro_dataframe = pd.DataFrame([], )
    for arg in args:
        statistic_shapiro, p_value_shapiro = stats.shapiro(arg)
        if p_value_shapiro < 0.05:
            interpretation = "La modalité ne suit pas une distribution normale."
            anova_validity = False
        else:
            interpretation = "La modalité suit une distribution normale."

        shapiro_row = pd.DataFrame([[mods[i], statistic_shapiro, p_value_shapiro, interpretation]], columns=['Modalité', 'Statistique', 'P-value', 'Interprétation'] )
        shapiro_dataframe = pd.concat([shapiro_dataframe, shapiro_row])

        i = i + 1
    shapiro_dataframe.to_excel(writer, sheet_name='Test Shapiro-Wilk', index=False)

    # Test de Levene
    statistic_levene, p_value_levene = stats.levene(*args, center="mean")
    if p_value_levene < 0.05:
        interpretation = "Les variances des populations ne sont pas homogènes."
        anova_validity = False
    else:
        interpretation = "Les variances des populations sont homogènes."
    levene_dataframe = pd.DataFrame({"Statistiques": [statistic_levene], "P-value": [p_value_levene], "Interprétation": interpretation})
    levene_dataframe.to_excel(writer, sheet_name='Test Levene', index=False)

    # Anova one-way
    statistic_anova, p_value_anova = stats.f_oneway(*args)
    if p_value_anova < 0.05:
        interpretation = "Il y a une différence entre les moyennes des modalités."
    else:
        interpretation = "Il n'y a pas de différence entre les moyennes des modalités."
    anova_dataframe = pd.DataFrame({"Statistiques": [statistic_anova], "P-value": [p_value_anova], "Interprétation": interpretation})
    anova_dataframe.to_excel(writer, sheet_name='Test ANOVA', index=False)

    if anova_validity:
        kruskal_dataframe = pd.DataFrame([], )
    else:
        statistic_kruskal, p_value_kruskal = stats.kruskal(*args)
        if p_value_kruskal < 0.05:
            interpretation = "Au moins un échantillon domine stochastiquement un autre échantillon."
        else:
            interpretation = "Il n'y a pas de différences entre les échantillons."
        kruskal_dataframe = pd.DataFrame({"Statistiques": [statistic_kruskal], "P-value": [p_value_kruskal], "Interprétation": interpretation})
        kruskal_dataframe.to_excel(writer, sheet_name='Test Kruskal-Wallis', index=False)

    return shapiro_dataframe, levene_dataframe, anova_dataframe, kruskal_dataframe
