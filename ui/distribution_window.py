from tkinter import *
from tkinter import filedialog

import pandas as pd

from functions.distribution import distribution_bar


def distribution_window():
    # Fenêtre
    window = Tk()
    window.title("Distribution")
    window.geometry("640x480")
    window.minsize(480, 360)
    window.config(background="#FFFFFF")

    # Titre de la page
    label_title = Label(window, text="Distributions", font="Helvetica, 40", bg="#FFFFFF", fg="#000000")
    label_title.pack()
    # Importer fichier
    filename = StringVar()

    def select_file():
        filename.set(filedialog.askopenfilename(
            title='Choisir le fichier excel',
        ))
        data = pd.read_excel(filename.get())

        # Menu variable
        variable = StringVar()

        def variable_selected(event):
            variable.set(clicked.get())

        options = data.columns.values
        clicked = StringVar()
        clicked.set(options[0])
        variable_list = OptionMenu(window, clicked, *options, command=variable_selected)
        variable_list.pack(pady=20)

        # Limite
        label_limit = Label(window, text="Limite (si 0, sans limite)", font="Helvetica, 20", bg="#FFFFFF", fg="#000000")
        label_limit.pack()

        default_limit = StringVar(window, value='0')
        limit_input = Entry(window, bg="#FFFFFF", fg="#000000", textvariable=default_limit)
        limit_input.pack(pady=20)

        # Exporter résultat
        directory = StringVar()

        def select_directory():
            directory.set(filedialog.askdirectory(
                title='Choisir la destination',
            ))

            def validation():
                distribution_bar(data, variable.get(), True, True, directory.get(),
                                 int(limit_input.get()))

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
