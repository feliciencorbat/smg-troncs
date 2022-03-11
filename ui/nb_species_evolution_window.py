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

    # Avec cf.
    with_cf = BooleanVar()
    with_cf.set(True)
    cf_check = Checkbutton(window, text="Avec espèces cf.", variable=with_cf,
                           onvalue=True, offvalue=False)
    cf_check.pack(pady=15)

    def validation():
        nb_species_evolution(with_cf)

        window.destroy()

    # Bouton validation
    validation_button = Button(window, text="Valider", command=validation)
    validation_button.pack()


    window.mainloop()