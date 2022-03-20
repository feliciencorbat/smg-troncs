import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns

"""
Matrice Cramer
"""


def cramer_matrix(data: pd.DataFrame) -> None:

    # dossier d'export
    directory = "export/cramer"
    if not os.path.exists(directory):
        os.makedirs(directory)

    print("\nMatrice V de Cramer (variables qualitatives)\n")

    data = data[["Saison", "Mois", "Nom", "LR", "Menace", "Substrat", "Espèce du substrat", "Groupe troncs"]]
    data = data.dropna()

    matrix = pd.DataFrame(index=data.columns, columns=data.columns)

    no_row = 1
    for rowIndex, row in matrix.iterrows():
        no_column = 1
        for columnIndex, value in row.items():
            if no_row >= no_column:
                cramer_value = cramer(data, str(rowIndex), str(columnIndex))
                matrix.loc[rowIndex].at[columnIndex] = cramer_value
            no_column = no_column + 1
        no_row = no_row + 1

    matrix = matrix.astype(float)
    print(matrix)

    writer = pd.ExcelWriter(directory + '/donnees.xlsx', engine='xlsxwriter')
    matrix.to_excel(writer, sheet_name='Matrice V de Cramer')
    writer.save()

    sns.heatmap(matrix, annot=matrix, vmin=0, vmax=1,
                cbar_kws={'label': 'Dépendance entre les variables qualitatives (0: faible, 1: élevée)'})
    plt.title("Matrice V de Cramer (variables qualitatives)", fontsize=16)
    plt.savefig(directory + "/matrice_cramer.png", bbox_inches='tight')
    plt.show(block=False)


def cramer(data: pd.DataFrame, variable1: str, variable2: str) -> float:
    contingency = pd.crosstab(data[variable1], data[variable2])
    chi2 = stats.chi2_contingency(contingency, correction=False)[0]
    n = np.sum(contingency).sum()
    min_dim = min(contingency.shape) - 1
    result = np.sqrt((chi2 / n) / min_dim)
    return result