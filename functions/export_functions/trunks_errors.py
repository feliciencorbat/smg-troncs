import pandas as pd


def trunks_errors(data: pd.DataFrame) -> pd.DataFrame:
    errors = pd.DataFrame([], )

    # Erreurs: Espèce du tronc absente
    species_trunk_errors = data[data['Espèce du substrat_right'].isnull()]
    species_trunk_errors = species_trunk_errors[['Espèce']]
    species_trunk_errors["Type d'erreur"] = "Tronc absent dans la feuille Troncs"
    species_trunk_errors["Ligne"] = species_trunk_errors.index + 2
    errors = pd.concat([errors, species_trunk_errors])

    # Erreurs: Incohérence dans l'espèce du tronc
    species_trunk_errors = data[(data['Espèce du substrat'] != data['Espèce du substrat_right'])
                                & data['Espèce du substrat_right'].notnull()]
    species_trunk_errors = species_trunk_errors[['Espèce']]
    species_trunk_errors["Type d'erreur"] = "Incohérence dans l'espèce du tronc"
    species_trunk_errors["Ligne"] = species_trunk_errors.index + 2
    errors = pd.concat([errors, species_trunk_errors])

    return errors
