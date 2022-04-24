import numpy as np
import pandas as pd


def new_threat_column(species: pd.DataFrame) -> pd.DataFrame:

    # Création colonne Menace
    conditions = [
        (species['Fréq'] == 'R'),
        (species['Fréq'] == 'AR'),
        (species['LR'] == 'EX'),
        (species['LR'] == 'EW'),
        (species['LR'] == 'RE'),
        (species['LR'] == 'CR'),
        (species['LR'] == 'EN'),
        (species['LR'] == 'VU'),
        (species['LR'] == 'LC'),
        (species['LR'] == 'NT')
    ]
    choices = [
        'Menacé',
        'Menacé',
        'Eteint',
        'Eteint',
        'Eteint',
        'Menacé',
        'Menacé',
        'Menacé',
        'Non menacé',
        'Menacé'
    ]
    species["Menace"] = np.select(condlist=conditions, choicelist=choices, default='Menace inconnue')

    return species
