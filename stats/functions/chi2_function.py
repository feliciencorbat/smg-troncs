import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

"""
Fonction Chi-2 entre 2 variables qualitatives et création heatmap
"""


def chi2_function(data: pd.DataFrame, variable1: str, variable2: str, title: str, species_agg: bool,
                  with_cf: bool, location: str, minimum: int):
    # Filtrer lieu
    if location != "Tous les lieux":
        data = data.loc[data["Lieu"] == location]

    # Si sans cf
    if not with_cf:
        data = data.loc[data["cf"] != "cf."]

    if minimum > 0:
        contingency2 = pd.crosstab(data[variable1], data[variable2], margins=True)
        for index, value in contingency2["All"].items():
            if value < minimum:
                data = data.loc[data[variable1] != index]

        contingency2 = pd.crosstab(data[variable1], data[variable2], margins=True)
        var2 = contingency2.iloc[-1]
        for index, value in var2.items():
            if value < minimum:
                data = data.loc[data[variable2] != index]

    # Si aggrégation par nom binomial
    if species_agg:
        contingency = data.pivot_table(values="Nom", index=variable1, columns=variable2,
                                       aggfunc=pd.Series.nunique, fill_value=0)
    else:
        contingency = pd.crosstab(data[variable1], data[variable2])

    # dossier d'export
    directory = "files/chi2"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # création du tableau des effectifs attendus (expected)
    chi2, p_value, deg_freedom, expected = stats.chi2_contingency(contingency)

    # vérification d'équivalence (stats.chisquare)
    if not (chi2, p_value) == stats.chisquare(contingency.to_numpy().ravel(), f_exp=expected.ravel(),
                                              ddof=contingency.size - 1 - deg_freedom):
        print("Problème avec stats.chisquare... les fréquences dans les catégories sont trop petites: "
              "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html")

    # transformation ndarray en dataframe
    expected = pd.DataFrame(data=expected, index=contingency.index, columns=contingency.columns)

    # création du tableau des différences
    differences = contingency - expected

    # récupérer la valeur absolue des différences
    absolute = differences / differences.abs()

    # création du tableau des contributions à la dépendance (0 = faible, 1 ou -1 = forte)
    dependence_contribution = (((contingency - expected) ** 2 * absolute / expected) / chi2)

    if expected.min().min() < 5:
        print("\nAttention, il y a dans le tableau des effectifs attendus une ou des valeurs inférieures à 5."
              "\nCela peut rendre le test chi-2 caduque.")

    # Liste des contributions à la dépendance triées
    sorted_dependance_contribution = pd.DataFrame([], )
    for rowIndex, row in dependence_contribution.iterrows():
        for columnIndex, value in row.items():
            row = pd.DataFrame({variable1: [rowIndex],
                                variable2: [columnIndex],
                                'Degré de dépendance': [value],
                                'Degré de dépendance absolu': [abs(value)]
                                })
            sorted_dependance_contribution = pd.concat([sorted_dependance_contribution, row], ignore_index=True, axis=0)

    sorted_dependance_contribution = sorted_dependance_contribution.sort_values(by=['Degré de dépendance absolu'],
                                                                                ascending=False)
    # Enregistrer le fichier excel
    writer = pd.ExcelWriter(directory + '/chi2.xlsx', engine='xlsxwriter')
    pd.DataFrame(data={'P_value': [p_value], 'Chi2': [chi2], 'Degré liberté': [deg_freedom]}) \
        .to_excel(writer, sheet_name='P_value, Chi2, Deg', index=False)
    contingency.to_excel(writer, sheet_name='Tab contingence')
    expected.to_excel(writer, sheet_name='Effectifs attendus')
    differences.to_excel(writer, sheet_name='Différences')
    dependence_contribution.to_excel(writer, sheet_name='Contribution dépendance')
    sorted_dependance_contribution.to_excel(writer, sheet_name='Contribution dépendance triée', index=False)
    writer.save()

    # création du graphe des contributions à la dépendance
    plt.figure()
    sns.heatmap(dependence_contribution,
                annot=contingency, fmt='d', vmin=-1, vmax=1, cmap="PiYG",
                cbar_kws={'label': 'Contribution à la dépendance'})
    plt.title(title, fontsize=16)
    plt.savefig(directory + "/dependance_contribution_heatmap.svg", bbox_inches='tight')

    # création du graphe à barres
    plt.figure()
    contingency.plot(kind="bar")
    if species_agg:
        plt.ylabel("Nombre d'espèces")
    else:
        plt.ylabel("Nombre d'observations")
    plt.title(title)
    plt.savefig(directory + "/contingence_bar.svg", bbox_inches='tight')

    return p_value, chi2, deg_freedom, contingency, expected, differences, dependence_contribution
