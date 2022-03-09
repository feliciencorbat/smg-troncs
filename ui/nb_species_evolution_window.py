from tkinter import *
from tkinter import filedialog
from functions.nb_species_evolution import nb_species_evolution


def nb_species_evolution_window():
    # Fenêtre
    window = Toplevel()
    window.title("Evolution du nombre d'espèces")
    window.geometry("640x480")
    window.minsize(480, 360)

    # Titre de la page
    label_title = Label(window, text="Evolution du nombre d'espèces", font="Helvetica, 20")
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

        def validation():
            nb_species_evolution(filename.get())

            window.destroy()

        # Bouton validation
        validation_button = Button(window, text="Valider", command=validation)
        validation_button.pack()

    open_file_button = Button(
        window,
        text='Choisir le fichier excel',
        command=select_file
    )
    open_file_button.pack(pady=15)

    window.mainloop()
