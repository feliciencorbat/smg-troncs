import pandas as pd


def new_swiss_fungi_link_column(species: pd.DataFrame) -> pd.DataFrame:
    species['SwissFungi Lien'] = species['SwissFungi'].apply(lambda x: make_hyperlink(x))
    return species


def make_hyperlink(value):
    url = "https://www.wsl.ch/map_fungi/search?lang=fr&taxon={}"
    if value is not None:
        return '=HYPERLINK("%s", "%s")' % (url.format(value), "Lien")
    else:
        return None
