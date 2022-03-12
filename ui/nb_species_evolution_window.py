from tkinter import *
from tkinter import filedialog

import numpy as np
import pandas as pd

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

    data = pd.read_excel("export/liste_modifiee.xlsx", sheet_name="Sheet1")

    # Menu lieu
    options = data["Lieu"].unique()
    options = np.append(options, ["Tous les lieux"])
    location = StringVar()
    location.set("Tous les lieux")

    def location_selected(event):
        location.set(location_clicked.get())

    location_clicked = StringVar()
    location_clicked.set("Tous les lieux")

    location_list = OptionMenu(window, location_clicked, *options, command=location_selected)
    location_list.pack(pady=15)

    # Avec cf.
    with_cf = BooleanVar()
    with_cf.set(True)
    cf_check = Checkbutton(window, text="Avec espèces cf.", variable=with_cf,
                           onvalue=True, offvalue=False)
    cf_check.pack(pady=15)

    def validation():
        nb_species_evolution(data, with_cf.get(), location.get())

        window.destroy()

    # Bouton validation
    validation_button = Button(window, text="Valider", command=validation)
    validation_button.pack()


    window.mainloop()