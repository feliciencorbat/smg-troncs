import numpy as np
import pandas as pd


def new_cut_trunks_dataframe(trunks: pd.DataFrame) -> pd.DataFrame:

    # Création du nouveau dataframe de coupe des troncs
    cut_trunks = trunks[["Identifiant", "Coupé entre"]].copy()
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].astype(str)
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].str.replace("?", "", regex=False)
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].str.replace("-", "", regex=False)
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].str.replace("hiver", "", regex=False)
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].str.replace("Hiver", "", regex=False)
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].str.replace(" ", "", regex=False)
    cut_trunks["Coupé entre"] = cut_trunks["Coupé entre"].replace('', np.nan)
    cut_trunks = cut_trunks.dropna()
    cut_trunks["Coupé début"] = pd.to_datetime(((cut_trunks["Coupé entre"].str[:4]) + "0101").astype(int),
                                               format='%Y%m%d')
    cut_trunks["Coupé fin"] = pd.to_datetime(((cut_trunks["Coupé entre"].str[-4:]) + "1231").astype(int),
                                             format='%Y%m%d')
    cut_trunks["Date de coupe"] = cut_trunks["Coupé début"] + ((cut_trunks["Coupé fin"] - cut_trunks["Coupé début"]) / 2)
    cut_trunks = cut_trunks[["Identifiant", "Date de coupe"]]

    return cut_trunks
