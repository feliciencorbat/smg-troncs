import pandas as pd
from docx import Document

def docx_generation(rare_species_maillettes: pd.DataFrame, rare_species_bossy: pd.DataFrame, year):

    document = Document()

    pre_title = document.add_paragraph('')
    pre_title.add_run("Observation et évolution des espèces fongiques sur les troncs du chemin des Maillettes et de ceux de la route du Pont de Bossy").bold = True

    document.add_paragraph('')

    document.add_heading("Rapport intermédiaire " + year, level=0)

    introduction_title = document.add_paragraph('')
    introduction_title.add_run('Introduction :').bold = True

    document.add_paragraph('De nombreux champignons de la liste rouge des espèces menacées en Suisse croissent sur de vieux arbres morts, de grands diamètres, principalement de feuillus. De tels arbres sont rarement rencontrés en forêt et par conséquent une niche écologique manque souvent pour ces espèces. Afin de créer un biotope favorable pour ces champignons, des troncs de feuillus de grands diamètres (chênes et peupliers principalement, mais aussi de saule et de marronniers) ont été déposés au sol, en bordure d’une route, en lisière de forêt, sur un sol humide.')
    document.add_paragraph('Un suivi mycologique régulier a été entrepris dès 2014.')

    annexes = document.add_paragraph('')
    annexes.add_run('Annexes :').bold = True

    document.add_paragraph('Tableau 3 : Nouvelles espèces de la liste rouge, rares ou assez rares trouvées en ' + year + ' sur les troncs du chemin des Maillettes')
    document.add_paragraph('Tableau 4 : Nouvelles espèces de la liste rouge, rares ou assez rares trouvées en ' + year + ' sur les troncs du chemin de Bossy')

    document.add_page_break()

    annexe3 = document.add_paragraph('')
    annexe3.add_run('Tableau 3 : Nouvelles espèces de la liste rouge, rares ou assez rares trouvées en ' + year + ' sur les troncs du chemin des Maillettes').bold = True

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Espèce'
    hdr_cells[1].text = 'Espèce actuelle'
    hdr_cells[2].text = 'Statut liste rouge'
    for index, row in rare_species_maillettes.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(row["Espèce"])
        row_cells[1].text = str(row["Espèce actuelle"])
        row_cells[2].text = str(row["Liste rouge"])

    document.add_page_break()

    annexe4 = document.add_paragraph('')
    annexe4.add_run(
        'Tableau 4 : Nouvelles espèces de la liste rouge, rares ou assez rares trouvées en ' + year + ' sur les troncs du chemin de Bossy').bold = True

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Espèce'
    hdr_cells[1].text = 'Espèce actuelle'
    hdr_cells[2].text = 'Statut liste rouge'
    for index, row in rare_species_bossy.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(row["Espèce"])
        row_cells[1].text = str(row["Espèce actuelle"])
        row_cells[2].text = str(row["Liste rouge"])

    document.add_page_break()

    return document
