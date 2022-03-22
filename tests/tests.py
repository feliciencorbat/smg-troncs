import shutil
import unittest

import pandas as pd

from functions.anova import anova_test
from functions.chi2 import chi2_test
from functions.cramer import cramer_matrix
from functions.distribution import distribution_bar
from functions.export import export
from functions.nb_species_evolution import nb_species_evolution


class Tests(unittest.TestCase):

    def test_functions(self):
        print("Test de l'export sans GBIF")
        export("liste_originale.xls", False)

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

        print("Test de l'export avec GBIF")
        export("liste_originale.xls", True)

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
