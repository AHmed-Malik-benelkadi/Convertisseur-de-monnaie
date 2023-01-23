#!/usr/bin/python
from tkinter import *
import tkinter as tk
from tkinter  import messagebox
import os
import json

window = tk.Tk()
window.title("Convertisseur de Monnaie")
# definition de la taille de l'interfacce
window.geometry("450x300")
window.configure(background="Azure")
window.iconbitmap("logo.ico")
titre = Label(window, text = "HELLO ! ",fg = 'red')
titre.pack()
window.resizable(0, 0)

amount_frame = tk.Frame(window)
amount_frame.pack()
label_amount = tk.Label(amount_frame, text="Montant:")
label_amount.pack(side='left')
entry_amount = tk.Entry(amount_frame)
entry_amount.pack(side='left')

from_frame = tk.Frame(window)
from_frame.pack()
label_from = tk.Label(from_frame, text="De:")
label_from.pack(side='left')
from_var = tk.StringVar(value='USD')
from_dropdown = tk.OptionMenu(from_frame, from_var, 'USD', 'EUR', 'JPY', 'Pound', 'CHF', )
from_dropdown.pack(side='right')

to_frame = tk.Frame(window)
to_frame.pack()
label_to = tk.Label(to_frame, text="À:")
label_to.pack(side='left')
to_var = tk.StringVar(value='EUR')
to_dropdown = tk.OptionMenu(to_frame, to_var, 'USD', 'EUR', 'JPY', 'Pound', 'CHF')
to_dropdown.pack(side='left')


history = []

def convert():
    amount = float(entry_amount.get())
    from_currency = from_var.get()
    to_currency = to_var.get()
    # taux de change fictif
    rates = {'USD': 1.0, 'EUR': 1.0, 'JPY': 105.0, 'Pound': 1.14, 'CHF': 1.0}
    is_valid = False
    while not is_valid:
        if from_currency in rates and to_currency in rates:
            result = amount * rates[to_currency] / rates[from_currency]
            label_result.config(text=str(result))
            # sauvegarder l'historique des conversions
            history.append((amount, from_currency, to_currency, result))
            is_valid = True
        else:
            label_result.config(text="Valeur non valide")
            is_valid = False

def show_history():
    if len(history) > 0:
        history_window = tk.Toplevel(window)
        history_window.title("Historique des conversions")
        i = 0
        while i < len(history):
            amount, from_currency, to_currency, result = history[i]
            history_label = tk.Label(history_window, text=f"{i + 1}. {amount} {from_currency} to {to_currency} = {result}")
            history_label.pack()
            i += 1
        close_button = tk.Button(history_window, text="Fermer", command=history_window.destroy)
        close_button.pack()
    else:
        tk.messagebox.showerror("Erreur", "Aucun historique disponible.")



def save():
    if os.path.exists("Historique.json"):
        with open("Historique.json", "a") as text_file:
            text_file.writelines(label_result.cget("text"))
            text_file.write("\n")
    else:
        with open("Historique.json", "w") as text_file:
            text_file.writelines(label_result.cget("text"))
            text_file.write("\n")
    text_file.close()


def add_new_currency():
    add_window = tk.Toplevel(window)
    add_window.title("Ajouter une devise")

    add_name_label = tk.Label(add_window, text="Nom de la devise : ")
    add_name_label.pack()
    add_name_entry = tk.Entry(add_window)
    add_name_entry.pack()

    add_rate_label = tk.Label(add_window, text="Taux de change : ")
    add_rate_label.pack()
    add_rate_entry = tk.Entry(add_window)
    add_rate_entry.pack()


    submit_button = tk.Button(add_window, text="Ajouter", command=lambda: add_currency(add_name_entry.get(), add_rate_entry.get()))
    submit_button.pack()

def add_currency(name, rate):
    if name not in rates:
        rates[name] = rate
        from_dropdown.config(menu=from_dropdown.children["menu"])
        from_dropdown["menu"].add_command(label=name, command=lambda: from_var.set(name))
        to_dropdown.config(menu=to_dropdown.children["menu"])
        to_dropdown["menu"].add_command(label=name, command=lambda: to_var.set(name))
    else:
        tk.messagebox.showerror("Erreur", "Cette devise existe déjà.")


convert_button = tk.Button(window, text="Convertir", command=convert, background="pink", cursor="mouse",relief="groove")
convert_button.pack()
history_btn = tk.Button(window, text="Sauvegarder", background="pink", cursor="mouse", relief="groove", command=save)
history_btn.pack()
result_frame = tk.Frame(window)
result_frame.pack()
label_result = tk.Label(result_frame, text="")
label_result.pack()

history_button = tk.Button(window, text="Historique", command=show_history, background="pink", cursor="mouse",relief="groove")
history_button.pack()

add_currency_button = tk.Button(window, text="Ajouter une devise", command=add_new_currency)
add_currency_button.pack(side="bottom")

currencies = []
rates = {}


window.mainloop()
