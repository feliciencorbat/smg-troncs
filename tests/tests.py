import shutil
import unittest

import pandas as pd

from stats.functions.anova_function import anova_function
from stats.functions.chi2_function import chi2_function
from stats.functions.cramer_function import cramer_function
from stats.functions.distribution_function import distribution_function
from stats.functions.export_function import export_function
from stats.functions.nb_species_evolution_function import nb_species_evolution_function


class Tests(unittest.TestCase):

    def test_functions(self):
        print("Test de l'export")
        export_function("liste_originale.xls")

        data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")

        print("Test de la fonction de distribution")
        distribution_function(data, "Espèce", "Titre du graphe", 20, True, "Tous les lieux")

        print("Test matrice Cramer")
        cramer_function(data, True, "Tous les lieux")

        print("Test de la fonction chi 2")
        chi2_function(data, "Espèce du tronc", "Menace", "Titre du graphe", False,
                  True, "Tous les lieux")

        print("Test de la fonction ANOVA")
        anova_function(data, "Menace", "Age du tronc", "Titre du graphe", True, "Tous les lieux")

        print("Test de la fonction évolution espèces")
        nb_species_evolution_function(data, True, "Tous les lieux")

        print("Effacer dossier export")
        shutil.rmtree("export")


if __name__ == '__main__':
    unittest.main()
