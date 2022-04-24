import shutil
import unittest

import pandas as pd

from stats.functions.anova_function import anova_test
from stats.functions.chi2_function import chi2_test
from stats.functions.cramer_function import cramer_matrix
from stats.functions.distribution_function import distribution_bar
from stats.functions.export_function import export
from stats.functions.nb_species_evolution import nb_species_evolution


class Tests(unittest.TestCase):

    def test_functions(self):
        print("Test de l'export")
        export("liste_originale.xls")

        data = pd.read_excel("export/liste_modifiee.xlsx", sheet_name="Statistiques")

        print("Test de la fonction de distribution")
        distribution_bar(data, "Espèce", "Titre du graphe", 20, True, "Tous les lieux")

        print("Test matrice Cramer")
        cramer_matrix(data, True, "Tous les lieux")

        print("Test de la fonction chi 2")
        chi2_test(data, "Espèce du tronc", "Menace", "Titre du graphe", False,
                  True, "Tous les lieux")

        print("Test de la fonction ANOVA")
        anova_test(data, "Menace", "Age du tronc", "Titre du graphe", True, "Tous les lieux")

        print("Test de la fonction évolution espèces")
        nb_species_evolution(data, True, "Tous les lieux")

        print("Effacer dossier export")
        shutil.rmtree("export")


if __name__ == '__main__':
    unittest.main()
