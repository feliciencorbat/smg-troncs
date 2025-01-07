class Constants:
    # Nombre de threads pour les requêtes gbif et swissfungi
    nb_workers = 16

    # Espèces avec orthographe fixée
    default_species_writing = ["Grandinia nespori", "Lenzites betulina", "Panellus stypticus",
                               "Phlebia cremeo-alutacea", "Pluteus podospileus fo. podospileus"]

    # Espèces dont la synonymie GBIF est refusée
    gbif_synonyms_errors = ["Tubaria hiemalis", "Galerina autumnalis", "Pluteus brunneoradiatus", "Diatrype undulata", "Coniophora arida var. suffocata", "Pluteus pallescens", "Aegerita tortuosa", "Pluteus podospileus fo. minutissimus"]
