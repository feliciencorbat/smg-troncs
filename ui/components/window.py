from tkinter import *
import pandas as pd


def window_title(title: str, with_data: bool = True):

    # Fenêtre
    window = Toplevel()

    window.title(title)
    window.geometry("480x480-500+0")
    window.minsize(480, 360)

    # Titre de la page
    label_title = Label(window, text=title, font="Helvetica, 20")
    label_title.pack()

    if with_data:
        data = pd.read_excel("export/liste_modifiee.xlsx", sheet_name="Statistiques")
        return window, data
    else:
        return window
