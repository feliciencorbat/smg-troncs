from tkinter import *
import numpy as np
from functions.cramer import cramer_matrix
from ui.components.window import window_title


def cramer_window():
    window, data = window_title("Matrice V de Cramer")

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

    # Avec cf.
    with_cf = BooleanVar()
    with_cf.set(True)
    cf_check = Checkbutton(window, text="Avec espèces cf.", variable=with_cf,
                           onvalue=True, offvalue=False)
    cf_check.pack()

    def validation():
        cramer_matrix(data, with_cf.get(), location.get())
        window.destroy()

    # Bouton de validation
    validation_button = Button(window, text="Valider", command=validation)
    validation_button.pack(pady=15)

    window.mainloop()
