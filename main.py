from tkinter import *
from ui.chi2_window import chi2_window
from ui.distribution_window import distribution_window
from ui.excel_window import excel_window

window = Tk()

window.title("Statistiques Troncs SMG")
window.geometry("640x480")
window.minsize(480, 360)
window.config(background="#FFFFFF")

frame = Frame(window, bg="#FFFFFF")

label_title = Label(frame, text="Statistiques Troncs SMG", font="Helvetica, 40", bg="#FFFFFF", fg="#000000")
label_title.pack()

excel_button = Button(frame, text="Générer nouveau fichier excel", font="Helvetica, 20", bg="#FFFFFF", fg="#000000",
                      command=excel_window)
excel_button.pack(pady=20)

distr_button = Button(frame, text="Distribution", font="Helvetica, 20", bg="#FFFFFF", fg="#000000",
                      command=distribution_window)
distr_button.pack(pady=20)

chi2_button = Button(frame, text="Test Chi-2", font="Helvetica, 20", bg="#FFFFFF", fg="#000000", command=chi2_window)
chi2_button.pack(pady=20)

frame.pack()

window.mainloop()

