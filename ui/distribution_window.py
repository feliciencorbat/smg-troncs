from tkinter import *
import numpy as np

from stats.functions.distribution_function import distribution_bar
from ui.components.window import window_title


def distribution_window():

    window, data = window_title("Distribution")

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

    # Menu variable
    variable = StringVar()

    def variable_selected(event):
        variable.set(clicked.get())

    options = data.columns.values
    clicked = StringVar()
    clicked.set("Choisir la variable...")
    variable_list = OptionMenu(window, clicked, *options, command=variable_selected)
    variable_list.pack(pady=15)

    # Titre du graphe
    default_title = StringVar(window, value="Titre du graphe")
    title_input = Entry(window, textvariable=default_title)
    title_input.pack(pady=15)

    # Limite
    label_limit = Label(window, text="Limite (si 0, sans limite)")
    label_limit.pack()

    default_limit = StringVar(window, value='0')
    limit_input = Entry(window, textvariable=default_limit)
    limit_input.pack(pady=15)

    # Avec cf.
    with_cf = BooleanVar()
    with_cf.set(True)
    cf_check = Checkbutton(window, text="Avec espèces cf.", variable=with_cf,
                           onvalue=True, offvalue=False)
    cf_check.pack(pady=15)

    def validation():
        distribution_bar(data, variable.get(), default_title.get(), int(limit_input.get()), with_cf.get(), location.get())

        window.destroy()

    # Bouton validation
    validation_button = Button(window, text="Valider", command=validation)
    validation_button.pack(pady=15)

    window.mainloop()
