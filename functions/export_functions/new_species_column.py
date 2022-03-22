import pandas as pd


def new_species_column(data: pd.DataFrame) -> pd.DataFrame:

    # Enlever les cf., ? et parenthèses des genres et espèces
    data["Genre"] = data["Genre"].str.replace(r"\(.*?\)", "", regex=True)
    data["Genre"] = data["Genre"].str.replace("cf.", "", regex=False)
    data["Genre"] = data["Genre"].str.replace("cf", "", regex=False)
    data["Genre"] = data["Genre"].str.replace("?", "", regex=False)
    data["Genre"] = data["Genre"].str.strip()

    data["Espèce"] = data["Espèce"].str.replace(r"\(.*?\)", "", regex=True)
    data["Espèce"] = data["Espèce"].str.replace("cf.", "", regex=False)
    data["Espèce"] = data["Espèce"].str.replace("cf", "", regex=False)
    data["Espèce"] = data["Espèce"].str.replace("?", "", regex=False)
    data["Espèce"] = data["Espèce"].str.strip()

    data.drop(['Genre', 'Espèce'], axis=1)

    # Création colonne Espèce
    data["Espèce"] = data["Genre"] + " " + data["Espèce"]

    return data
