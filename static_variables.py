from classes.species import Species


class StaticVariables:
    default_species_writing = ["Grandinia nespori", "Lenzites betulina", "Panellus stypticus",
                               "Phlebia cremeo-alutacea", "Pluteus podospileus fo. podospileus"]

    gbif_synonyms_errors = {"Tubaria hiemalis": Species("Tubaria hiemalis", "Basidiomycota", "Agaricales", "SPECIES"),
                            "Galerina autumnalis":
                                Species("Galerina autumnalis", "Basidiomycota", "Agaricales", "SPECIES")
                            }
