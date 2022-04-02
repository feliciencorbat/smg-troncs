import pandas as pd


def lr_errors(species: pd.DataFrame) -> pd.DataFrame:

    errors = pd.DataFrame([], )

    # Chercher les incohérences entre la LR et la SwissFungi LR
    species_lr = species[['Espèce', 'LR', "SwissFungi LR"]].dropna()

    species_lr_errors = species_lr[(species_lr['LR'] != species_lr['SwissFungi LR'])]
    species_lr_errors = species_lr_errors[['Espèce']]
    species_lr_errors["Type d'erreur"] = "Incohérence dans la liste rouge entre LR et SwissFungi LR"
    errors = pd.concat([errors, species_lr_errors])

    return errors
