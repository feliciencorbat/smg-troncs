from tkinter import *
from tkinter import filedialog
from functions.export import export


def excel_window():
    # Fenêtre
    window = Toplevel()
    window.title("Générer le fichier excel pour les statistiques")
    window.geometry("640x640")
    window.minsize(480, 360)

    # Titre de la page
    label_title = Label(window, text="Générer le fichier excel pour les statistiques", font="Helvetica, 20")
    label_title.pack()

    # Importer fichier
    filename = StringVar()

    # Label bouton de sélection du fichier
    label_select_file = Label(window, text="Le fichier à sélectionner est le fichier excel original."
                                           "\nIl doit obligatoirement contenir les feuilles Observations et Troncs.")
    label_select_file.pack(pady=15)

    def select_file():
        filename.set(filedialog.askopenfilename(
            title='Choisir le fichier excel à transformer',
        ))

        # Ajouter colonnes GBIF
        gbif_checked = BooleanVar()
        gbif = Checkbutton(window, text="Ajouter les colonnes GBIF avec le nom actuel et de la systématique.\n"
                                        "Cela nécessite internet et prend quelques minutes.\n"
                                        "Permet également de vérifier la synonymie.",
                           variable=gbif_checked, onvalue=True, offvalue=False)
        gbif.pack(pady=15)

        def validation():
            export(filename.get(), gbif_checked.get())

            window.destroy()

        # Bouton validation
        validation_button = Button(window, text="Valider", command=validation)
        validation_button.pack()

        # Label bouton de sélection du fichier
        label_validation = Label(window,
                                 text="Le fichier liste_modifiee.xlsx est créé dans le dossier export."
                                      "\n Ce dossier se trouve au même emplacement que le fichier original."
                                      "\n En plus, un fichier avec les erreurs et un fichier avec la liste "
                                      "des espèces y sont créés.")
        label_validation.pack(pady=15)

    open_file_button = Button(
        window, text='Choisir le fichier excel', command=select_file
    )
    open_file_button.pack()

    window.mainloop()
