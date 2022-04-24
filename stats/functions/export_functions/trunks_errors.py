import datetime

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

    # Erreurs: Age du tronc négatif
    age_trunk_errors = data[(data['Age du tronc'] < datetime.timedelta(seconds=0))]
    age_trunk_errors = age_trunk_errors[['Substrat']]
    age_trunk_errors["Type d'erreur"] = "L'âge est négatif pour le tronc " + age_trunk_errors['Substrat']
    age_trunk_errors["Espèce"] = ""
    age_trunk_errors["Ligne"] = age_trunk_errors.index + 2
    age_trunk_errors = age_trunk_errors[["Espèce", "Type d'erreur", "Ligne"]]
    errors = pd.concat([errors, age_trunk_errors])

    return errors
