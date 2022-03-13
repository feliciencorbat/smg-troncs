from tkinter import *

import numpy as np
import pandas as pd
from functions.chi2 import chi2_test


def chi2_window():
    # Fenêtre
    window = Toplevel()
    window.title("Test Chi-2")
    window.geometry("640x640")
    window.minsize(480, 360)

    # Titre de la page
    label_title = Label(window, text="Test Chi-2", font="Helvetica, 20")
    label_title.pack()

    data = pd.read_excel("export/liste_modifiee.xlsx", sheet_name="Statistiques")

    # Menu lieu
    options = data["Lieu"].dropna().unique()
    options = np.append(options, ["Tous les lieux"])
    location = StringVar()
    location.set("Tous les lieux")

    def location_selected(event):
        location.set(location_clicked.get())

    location_clicked = StringVar()
    location_clicked.set("Tous les lieux")

    location_list = OptionMenu(window, location_clicked, *options, command=location_selected)
    location_list.pack(pady=15)

    # Menu variable 1
    options = data.columns.values
    variable1 = StringVar()

    def variable1_selected(event):
        variable1.set(clicked1.get())

    clicked1 = StringVar()
    clicked1.set("Choisir la variable 1...")

    variable1_list = OptionMenu(window, clicked1, *options, command=variable1_selected)
    variable1_list.pack(pady=15)

    # Menu variable 2
    variable2 = StringVar()

    def variable2_selected(event):
        variable2.set(clicked2.get())

    clicked2 = StringVar()
    clicked2.set("Choisir la variable 2...")

    variable2_list = OptionMenu(window, clicked2, *options, command=variable2_selected)
    variable2_list.pack(pady=15)

    # Titre du graphe
    default_title = StringVar(window, value="Titre du graphe")
    title_input = Entry(window, textvariable=default_title)
    title_input.pack(pady=15)

    # Aggrégation nom binomial
    species_check = BooleanVar()
    species_agg = Checkbutton(window, text="Aggrégation espèce", variable=species_check,
                              onvalue=True, offvalue=False)
    species_agg.pack()

    # Avec cf.
    with_cf = BooleanVar()
    with_cf.set(True)
    cf_check = Checkbutton(window, text="Avec espèces cf.", variable=with_cf,
                           onvalue=True, offvalue=False)
    cf_check.pack()

    def validation():
        chi2_test(data, variable1.get(), variable2.get(), title_input.get(), species_check.get(),
                  with_cf.get(), location.get())
        window.destroy()

    # Bouton de validation
    validation_button = Button(window, text="Valider", command=validation)
    validation_button.pack(pady=15)

    window.mainloop()
