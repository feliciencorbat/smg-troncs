from tkinter import *
from tkinter import filedialog

import pandas as pd
from functions.chi2 import chi2_heatmap


def chi2_window():
    # Fenêtre
    window = Tk()
    window.title("Test Chi-2")
    window.geometry("640x640")
    window.minsize(480, 360)
    window.config(background="#FFFFFF")

    # Titre de la page
    label_title = Label(window, text="Test Chi-2", font="Helvetica, 40", bg="#FFFFFF", fg="#000000")
    label_title.pack()

    # Importer fichier
    filename = StringVar()

    def select_file():
        filename.set(filedialog.askopenfilename(
            title='Choisir le fichier excel',
        ))
        data = pd.read_excel(filename.get())

        # Titre variable 1
        label_variable1 = Label(window, text="Choix variable 1", font="Helvetica, 20", bg="#FFFFFF", fg="#000000")
        label_variable1.pack()

        # Menu variable 1
        options = data.columns.values
        variable1 = StringVar()

        def variable1_selected(event):
            variable1.set(clicked1.get())

        clicked1 = StringVar()
        clicked1.set(options[0])

        variable1_list = OptionMenu(window, clicked1, *options, command=variable1_selected)
        variable1_list.pack(pady=20)

        # Titre variable 2
        label_variable2 = Label(window, text="Choix variable 2", font="Helvetica, 20", bg="#FFFFFF", fg="#000000")
        label_variable2.pack()

        # Menu variable 2
        variable2 = StringVar()

        def variable2_selected(event):
            variable2.set(clicked2.get())

        clicked2 = StringVar()
        clicked2.set(options[0])

        variable2_list = OptionMenu(window, clicked2, *options, command=variable2_selected)
        variable2_list.pack(pady=20)

        # Titre du graphe
        label_title_graph = Label(window, text="Titre du graphe", font="Helvetica, 20", bg="#FFFFFF", fg="#000000")
        label_title_graph.pack()

        # Titre du graphe
        default_title = StringVar(window, value="Titre du graphe")
        title_input = Entry(window, bg="#FFFFFF", fg="#000000", textvariable=default_title)
        title_input.pack(pady=20)

        # Aggrégation nom binomial
        def checked():
            species_check.set(not species_check.get())

        species_check = BooleanVar()
        species_agg = Checkbutton(window, text="Aggrégation espèce",
                                  variable=species_check, bg="#FFFFFF", fg="#000000", command=checked)
        species_agg.pack()

        # Exporter résultat
        directory = StringVar()

        def select_directory():
            directory.set(filedialog.askdirectory(
                title='Choisir la destination',
            ))

            def validation():
                chi2_heatmap(data, variable1.get(),
                             variable2.get(), title_input.get(), True, True,
                             directory.get(), species_check.get())

                window.destroy()

            # Bouton de validation
            validation_button = Button(window, text="Valider", bg="#FFFFFF", borderwidth=0,
                                       command=validation, font="Helvetica, 20",
                                       fg="#000000")
            validation_button.pack()

        open_directory_button = Button(
            window,
            text='Choisir le dossier de destination du résultat',
            command=select_directory,
            font="Helvetica, 20",
            bg="#FFFFFF",
            fg="#000000"
        )
        open_directory_button.pack(pady=20)

    open_file_button = Button(
        window,
        text='Choisir le fichier excel',
        command=select_file,
        font="Helvetica, 20",
        bg="#FFFFFF",
        fg="#000000"
    )
    open_file_button.pack(pady=20)

    window.mainloop()
