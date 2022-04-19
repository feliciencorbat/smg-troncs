import pandas as pd


def test_nb_obs(data: pd.DataFrame, nb_obs) -> pd.DataFrame:
    errors = pd.DataFrame([], )

    if data.shape[0] != nb_obs:
        error_row = pd.DataFrame({'Espèce': [""],
                                  "Type d'erreur": ["Il y a un problème avec le nombre de lignes"]})
        errors = pd.concat([errors, error_row])
        print("Le nombre d'observations n'est pas le même que dans le fichier de départ.")
    else:
        print("Le nombre d'observations est le même que dans le fichier de départ.")

    return errors
