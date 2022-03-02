from tkinter import *
from tkinter import filedialog

import pandas as pd

from functions.new_list import new_list


def excel_window():
    # Fenêtre
    window = Tk()
    window.title("Test Chi-2")
    window.geometry("640x640")
    window.minsize(480, 360)
    window.config(background="#FFFFFF")

    # Titre de la page
    label_title = Label(window, text="Transformer le fichier excel", font="Helvetica, 40", bg="#FFFFFF", fg="#000000")
    label_title.pack()

    # Importer fichier
    filename = StringVar()

    def select_file():
        filename.set(filedialog.askopenfilename(
            title='Choisir le fichier excel à transformer',
        ))
        data = pd.read_excel(filename.get())

        # Ajouter colonnes GBIF
        def checked():
            gbif_checked.set(not gbif_checked.get())

        gbif_checked = BooleanVar()
        gbif = Checkbutton(window, text="Ajouter les colonnes GBIF (prend du temps et nécessite internet)",
                           variable=gbif_checked, bg="#FFFFFF", fg="#000000", command=checked)
        gbif.pack()

        # Exporter résultat
        directory = StringVar()

        def select_directory():
            directory.set(filedialog.askdirectory(
                title='Choisir la destination',
            ))

            def validation():
                new_list(data, directory.get(), gbif_checked.get())

                window.destroy()

            # Bouton validation
            validation_button = Button(window, text="Valider", bg="#FFFFFF", fg="#000000",
                                       command=validation, font="Helvetica, 20")
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
