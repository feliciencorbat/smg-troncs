import numpy as np
import pandas as pd


def new_date_columns(data: pd.DataFrame) -> pd.DataFrame:

    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    if data['Date'].isnull().any():
        raise ValueError("Certaines valeurs dans la colonne 'Date' ne peuvent pas être converties en format datetime.")


    # Création  colonne saison
    conditions = [
        (data['Date'].dt.month < 3),
        np.logical_and(data['Date'].dt.month == 3, data['Date'].dt.day < 21),
        (data['Date'].dt.month < 6),
        np.logical_and(data['Date'].dt.month == 6, data['Date'].dt.day < 21),
        (data['Date'].dt.month < 9),
        np.logical_and(data['Date'].dt.month == 9, data['Date'].dt.day < 21),
        (data['Date'].dt.month < 12),
        np.logical_and(data['Date'].dt.month == 12, data['Date'].dt.day < 21),
        np.logical_and(data['Date'].dt.month == 12, data['Date'].dt.day >= 21),
    ]
    choices = [
        'Hiver',
        'Hiver',
        'Printemps',
        'Printemps',
        'Eté',
        'Eté',
        'Automne',
        'Automne',
        'Hiver'
    ]

    try:
        data["Saison"] = np.select(condlist=conditions, choicelist=choices, default="Saison iconnue")
    except Exception as e:
        print(f"Une exception s'est produite dans le fichier new_date_columns : {e}")
        raise


    # Création colonne Mois
    data['Mois'] = data['Date'].dt.month

    # Création colonne Année
    data['Année'] = data['Date'].dt.year

    return data
