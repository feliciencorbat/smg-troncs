import pandas as pd


def synonyms_errors(species: pd.DataFrame) -> pd.DataFrame:

    errors = pd.DataFrame([], )

    # Chercher les synonymes
    species_synonyms = species[['Espèce', 'Espèce actuelle']].drop_duplicates()
    size = species_synonyms.groupby(['Espèce actuelle']).size()

    syn_errors = size[size >= 2].index
    for syn_error in syn_errors:
        print(syn_error + " a une synonymie")
        error_row = pd.DataFrame({'Espèce': [syn_error],
                                  "Type d'erreur": ["Il y a une synonymie détectée par GBIF"]})
        errors = pd.concat([errors, error_row])

    return errors
