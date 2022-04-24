import pandas as pd


def new_species_dataframe(data: pd.DataFrame) -> pd.DataFrame:

    # Création du nouveau dataframe species
    species = data[['Espèce', 'LR', 'Fréq']].drop_duplicates()
    species = species.sort_values("Espèce")

    return species
