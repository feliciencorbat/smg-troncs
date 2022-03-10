from tkinter import *
from tkinter import filedialog

import pandas as pd
from functions.chi2 import chi2_heatmap


def chi2_window():
    # Fenêtre
    window = Toplevel()
    window.title("Test Chi-2")
    window.geometry("640x640")
    window.minsize(480, 360)

    # Titre de la page
    label_title = Label(window, text="Test Chi-2", font="Helvetica, 20")
    label_title.pack()

    # Importer fichier
    filename = StringVar()

    # Label bouton de sélection du fichier
    label_select_file = Label(window, text="Le fichier à sélectionner est le fichier liste_modifiee.xlsx."
                                           "\nCe fichier se trouve dans le dossier export."
                                           "\nIl faut au préalable avoir généré le fichier excel pour les statistiques."
                              )
    label_select_file.pack(pady=15)

    def select_file():
        filename.set(filedialog.askopenfilename(
            title='Choisir le fichier excel',
        ))
        data = pd.read_excel(filename.get(), sheet_name="Sheet1")

        # Titre variable 1
        label_variable1 = Label(window, text="Choix variable 1")
        label_variable1.pack()

        # Menu variable 1
        options = data.columns.values
        variable1 = StringVar()

        def variable1_selected(event):
            variable1.set(clicked1.get())

        clicked1 = StringVar()
        clicked1.set("Choisir la variable 1...")

        variable1_list = OptionMenu(window, clicked1, *options, command=variable1_selected)
        variable1_list.pack(pady=20)

        # Titre variable 2
        label_variable2 = Label(window, text="Choix variable 2")
        label_variable2.pack()

        # Menu variable 2
        variable2 = StringVar()

        def variable2_selected(event):
            variable2.set(clicked2.get())

        clicked2 = StringVar()
        clicked2.set("Choisir la variable 2...")

        variable2_list = OptionMenu(window, clicked2, *options, command=variable2_selected)
        variable2_list.pack(pady=20)

        # Titre du graphe
        label_title_graph = Label(window, text="Titre du graphe")
        label_title_graph.pack()

        # Titre du graphe
        default_title = StringVar(window, value="Titre du graphe")
        title_input = Entry(window, textvariable=default_title)
        title_input.pack(pady=20)

        # Aggrégation nom binomial
        species_check = BooleanVar()
        species_agg = Checkbutton(window, text="Aggrégation espèce", variable=species_check,
                                  onvalue=True, offvalue=False)
        species_agg.pack()

        def validation():
            chi2_heatmap(data, filename.get(), variable1.get(), variable2.get(), title_input.get(), species_check.get())
            window.destroy()

        # Bouton de validation
        validation_button = Button(window, text="Valider", command=validation)
        validation_button.pack()

    open_file_button = Button(
        window, text='Choisir le fichier excel', command=select_file)
    open_file_button.pack()

    window.mainloop()
