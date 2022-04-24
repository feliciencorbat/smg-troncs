import pandas as pd


def new_cf_column(data: pd.DataFrame) -> pd.DataFrame:

    # Création colonne cf
    data['cf'] = data["Espèce"].str.contains('cf|\?', regex=True)
    data["cf"] = data["cf"].replace(False, "", regex=False)
    data["cf"] = data["cf"].replace(True, "cf.", regex=False)

    return data
