from tkinter import *
from tkinter import filedialog
from functions.export import export
from ui.components.window import window_title


def excel_window():

    window = window_title("Générer le fichier excel pour les statistiques", False)

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

        export(filename.get())

        window.destroy()

    open_file_button = Button(
        window, state="normal", text='Choisir le fichier excel', command=select_file
    )
    open_file_button.pack()

    # Label bouton de sélection du fichier
    label_validation = Label(window,
                             text="Le fichier liste_modifiee.xlsx est créé dans le dossier export."
                                  "\n Ce dossier se trouve au même emplacement que le projet python."
                                  "\n En plus, le fichier contient les feuilles avec les erreurs, la liste "
                                  "\ndes espèces et la liste des espèces par tronc.")
    label_validation.pack(pady=15)

    window.mainloop()
