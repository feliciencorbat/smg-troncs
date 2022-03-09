from tkinter import *
from tkinter import filedialog

import pandas as pd

from functions.distribution import distribution_bar


def distribution_window():
    # Fenêtre
    window = Toplevel()
    window.title("Distribution")
    window.geometry("640x480")
    window.minsize(480, 360)

    # Titre de la page
    label_title = Label(window, text="Distributions", font="Helvetica, 20")
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

        # Menu variable
        variable = StringVar()

        # Label variable
        label_limit = Label(window, text="Choisir la variable qualitative")
        label_limit.pack()

        def variable_selected(event):
            variable.set(clicked.get())

        options = data.columns.values
        clicked = StringVar()
        clicked.set("Choisir la variable...")
        variable_list = OptionMenu(window, clicked, *options, command=variable_selected)
        variable_list.pack(pady=20)

        # Titre du graphe
        label_title_graph = Label(window, text="Titre du graphe")
        label_title_graph.pack()

        # Titre du graphe
        default_title = StringVar(window, value="Titre du graphe")
        title_input = Entry(window, textvariable=default_title)
        title_input.pack(pady=20)

        # Limite
        label_limit = Label(window, text="Limite (si 0, sans limite)")
        label_limit.pack()

        default_limit = StringVar(window, value='0')
        limit_input = Entry(window, textvariable=default_limit)
        limit_input.pack(pady=20)

        def validation():
            distribution_bar(data, filename.get(), variable.get(), default_title.get(), int(limit_input.get()))

            window.destroy()

        # Bouton validation
        validation_button = Button(window, text="Valider", command=validation)
        validation_button.pack()

    open_file_button = Button(
        window,
        text='Choisir le fichier excel',
        command=select_file
    )
    open_file_button.pack()

    window.mainloop()
