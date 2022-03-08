from tkinter import *
from ui.chi2_window import chi2_window
from ui.distribution_window import distribution_window
from ui.export_window import excel_window

window = Tk()

window.title("Statistiques Troncs SMG")
window.geometry("640x480")
window.minsize(480, 360)

label_title = Label(window, text="Statistiques Troncs SMG", font="Helvetica, 20")
label_title.pack()

excel_button = Button(window, text="Générer le fichier excel pour les statistiques", command=excel_window)
excel_button.pack(pady=15)

distr_button = Button(window, text="Distribution (1 variable)", command=distribution_window)
distr_button.pack(pady=15)

chi2_button = Button(window, text="Test Chi-2 (2 variables qualitatives)", command=chi2_window)
chi2_button.pack(pady=15)

window.mainloop()

