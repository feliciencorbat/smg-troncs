"""
ACM (test)
"""
import pandas as pd
import prince


def mca(data: pd.DataFrame):
    data = data.drop(
        columns=['Genre', 'Espèce', 'Auteurs', 'Abondance', 'X', 'Y', 'Canton', 'Alt', 'Végétation', 'Photo', 'B/A/M',
                 'm/nm/i', 'Fréq', 'Legit', 'Dét', 'Exsiccata', 'Réf Litt Déter', 'Zone/Lieu', 'Date'])
    data.columns = ['Substrat', 'Espèce de substrat', 'LR', 'Nom binomial']
    print(data.head())

    mca = prince.MCA(
        n_components=2,
        n_iter=3,
        copy=True,
        check_input=True,
        engine='auto',
        random_state=42
    )

    mca = mca.fit(data)

    ax = mca.plot_coordinates(
        X=data,
        ax=None,
        figsize=(10, 10),
        show_row_points=True,
        row_points_size=10,
        show_row_labels=True,
        show_column_points=True,
        column_points_size=30,
        show_column_labels=False,
        legend_n_cols=1
    )
    ax.get_figure().savefig('export/mca_coordinates.svg')
    print(data.iloc[2679])