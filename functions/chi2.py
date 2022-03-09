import os
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns

"""
Fonction Chi-2 entre 2 variables qualitatives et création heatmap
"""


def chi2_heatmap(data: pd.DataFrame, filename: str, variable1: str, variable2: str, title: str, show_plot: bool,
                 export_files: bool, species_agg: bool) -> None:

    # Si aggrégation par nom binomial
    if species_agg:
        contingency = data.pivot_table(values="Nom", index=variable1, columns=variable2,
                                       aggfunc=pd.Series.nunique, fill_value=0)
    else:
        contingency = pd.crosstab(data[variable1], data[variable2])

    print("\nTest Chi-2 pour les variables " + contingency.index.name + " et " + contingency.columns.name + "\n")

    # dossier d'export
    dirname = os.path.dirname(filename)
    directory = dirname + "/chi2 " + contingency.index.name + " " + contingency.columns.name
    if not os.path.exists(directory):
        os.makedirs(directory)

    # affichage du tableau de contingence (contingency)
    print("Tableau de contingence\n")
    print(contingency)
    if export_files:
        contingency.to_excel(directory + "/tableau_contingence.xlsx")

    # création du tableau des effectifs attendus (expected)
    chi2, p_value, deg_freedom, expected = stats.chi2_contingency(contingency)

    # vérification d'équivalence (stats.chisquare)
    if not (chi2, p_value) == stats.chisquare(contingency.to_numpy().ravel(), f_exp=expected.ravel(),
                                              ddof=contingency.size - 1 - deg_freedom):
        print("Problème avec stats.chisquare... les fréquences dans les catégories sont trop petites: "
              "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html")

    # transformation ndarray en dataframe
    expected = pd.DataFrame(data=expected, index=contingency.index, columns=contingency.columns)
    print("\nTableau des effectifs attendus")
    print("Attention: il ne doit pas y avoir d'effectif inférieur à 5...\n")
    print(expected)
    if export_files:
        expected.to_excel(directory + "/tableau_effectifs_attendus.xlsx")

    # création du tableau des différences
    differences = contingency - expected
    print("\nTableau des différences\n")
    print(differences)
    if export_files:
        differences.to_excel(directory + "/tableau_differences.xlsx")

    # récupérer la valeur absolue des différences
    absolute = differences / differences.abs()

    # création du tableau des contributions à la dépendance (0 = faible, 1 ou -1 = forte)
    dependence_contribution = (((contingency - expected) ** 2 * absolute / expected) / chi2) * 100

    print("\nTableau des contribution à la dépendance\n")
    print(dependence_contribution)
    if export_files:
        dependence_contribution.to_excel(directory + "/tableau_contribution_dependance.xlsx")

    # affichage des données chi2, p-value, degré de liberté
    print("\nP-value: " + str(p_value) + "\n")
    print("Chi2: " + str(chi2) + "\n")
    print("Degré de liberté: " + str(deg_freedom) + "\n")

    if export_files:
        pd.DataFrame(data={'P_value': [p_value], 'Chi2': [chi2], 'Degré liberté': [deg_freedom]}) \
            .to_excel(directory + "/donnees_chi.xlsx", index=False)

    # création du graphe des contributions à la dépendance
    sns.heatmap(dependence_contribution,
                annot=contingency, fmt='d', vmin=-100, vmax=100, cmap="PiYG",
                cbar_kws={'label': 'Pourcentage contribution à la dépendance'})
    plt.title(title, fontsize=16)
    if export_files:
        plt.savefig(directory + "/dependance_contribution_heatmap.svg", bbox_inches='tight')
        plt.savefig(directory + "/dependance_contribution_heatmap.png", bbox_inches='tight')
    if show_plot:
        plt.show()


"""
Chi-2 compléments à intégrer
"""

# supprimer certaines colonnes et lignes (les colonnes inutiles, fusionnées ou manquant de données)
# contengency = contengency.drop(columns=['Menace inconnue'], index=['?', 'conifère'])

# renommer les axes
# contengency = contengency.rename_axis("Arbres", axis=0)
# contengency = contengency.rename_axis("Liste rouge", axis=1)
# contengency = contengency.rename(index={"saule": "Saule", "marronnier": "Marronnier", "chêne": "Chêne", "peuplier": "Peuplier"})
