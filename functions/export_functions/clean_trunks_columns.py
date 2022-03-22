import pandas as pd


def clean_trunks_columns(trunks: pd.DataFrame, data: pd.DataFrame):

    # Enlever les parenthèses, *, ... des identifiants des troncs
    trunks["Identifiant"] = trunks["Identifiant"].astype(str)
    trunks["Identifiant"] = trunks["Identifiant"].str.replace(r"\(.*?\)", "", regex=True)
    trunks["Identifiant"] = trunks["Identifiant"].str.replace("*", "", regex=False)
    trunks["Identifiant"] = trunks["Identifiant"].str.strip()

    data["Substrat"] = data["Substrat"].str.replace("tronc ", "", regex=False)
    data["Substrat"] = data["Substrat"].str.replace(r"\(.*?\)", "", regex=True)
    data["Substrat"] = data["Substrat"].str.strip()

    return trunks, data
