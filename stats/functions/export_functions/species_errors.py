import pandas as pd


def species_errors(data: pd.DataFrame, species: pd.DataFrame) -> pd.DataFrame:
    errors = pd.DataFrame([], )

    # Afficher les erreurs dans les espèces qui contiennent une parenthèse non fermée ou égal
    syn_errors = data.loc[data["Espèce"].str.contains(r'\)|\(|\=', case=False)]
    syn_errors = syn_errors[["Espèce"]]
    syn_errors["Type d'erreur"] = "Erreur de parenthèse non fermée ou de caractère indésirable"
    syn_errors["Ligne"] = syn_errors.index + 2
    errors = pd.concat([errors, syn_errors])

    # Chercher les incohérences entre Espèce et LR
    size = species.groupby(['Espèce']).size()
    lr_errors = size[size >= 2].index
    for lr_error in lr_errors:
        print(lr_error + " a une incohérence avec la liste rouge")
        error_row = pd.DataFrame({'Espèce': [lr_error],
                                  "Type d'erreur": ["Il y a une incohérence entre l'espèce et la liste rouge"]})
        errors = pd.concat([errors, error_row])

    return errors
