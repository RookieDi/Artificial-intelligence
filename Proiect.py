import tkinter as tk
from tkinter import ttk
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def step_function(x):
    return 1 if x > 0 else 0
#Aici trebe alta functie nu relu
def relu(x):
    return max(0, x)

def tanh(x):
    return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))

def linear(x):
    return x

def suma(valori):
    return sum(valori)

def produs(valori):
    result = 1
    for val in valori:
        result *= val
    return result

def minim(valori):
    return min(valori)

def maxim(valori):
    return max(valori)

def calcul_functii():
    valori = []
    try:
        for i in range(len(entries_input)):
            intrare = float(entries_input[i].get())
            greutate = float(entries_weight[i].get())
            valori.append(intrare * greutate)

        operatia = combo_operatii.get()
        if operatia == 'Sumă':
            rezultat = suma(valori)
        elif operatia == 'Produs':
            rezultat = produs(valori)
        elif operatia == 'Min':
            rezultat = minim(valori)
        elif operatia == 'Max':
            rezultat = maxim(valori)
        
       
        label_rezultat_intermediar.config(text=f"Rezultat intermediar: {rezultat:.4f}")
        return rezultat
    except ValueError:
        label_rezultat_intermediar.config(text="Eroare: Introduceți numere valide.")

def calcul_functii_activare():
    rezultat_intermediar = calcul_functii()  
    if rezultat_intermediar is not None: 
        activare = combo_activare.get()
        if activare == 'Sigmoid':
            rezultat_final = sigmoid(rezultat_intermediar)
        elif activare == 'Tanh':
            rezultat_final = tanh(rezultat_intermediar)
        elif activare == 'ReLU':
            rezultat_final = relu(rezultat_intermediar)
        elif activare == 'Linear':
            rezultat_final = linear(rezultat_intermediar)
        elif activare == 'Step':
            rezultat_final = step_function(rezultat_intermediar)

        label_rezultat.config(text=f"Rezultat final: {rezultat_final:.4f}")

def actualizeaza_neuroni():
    for widget in frame_neuroni.winfo_children():
        widget.destroy()

    global entries_input, entries_weight
    entries_input = []
    entries_weight = []
    
    numar_neuroni = int(nr_neuroni.get())
    for i in range(numar_neuroni):
        tk.Label(frame_neuroni, text=f"Neuron {i+1} - Intrare:").grid(row=i, column=0)
        entry_input = tk.Entry(frame_neuroni)
        entry_input.grid(row=i, column=1)
        entries_input.append(entry_input)
        
        tk.Label(frame_neuroni, text="Greutate:").grid(row=i, column=2)
        entry_weight = tk.Entry(frame_neuroni)
        entry_weight.grid(row=i, column=3)
        entries_weight.append(entry_weight)

window = tk.Tk()
window.title("Rețea Neuronală Simplă")
window.geometry("500x400")

nr_neuroni = ttk.Combobox(window, values=[i for i in range(1, 100)], width=5)  
nr_neuroni.set(1)
tk.Label(window, text="Număr de neuroni:").pack(pady=10)
nr_neuroni.pack()
nr_neuroni.bind("<<ComboboxSelected>>", lambda event: actualizeaza_neuroni())

frame_neuroni = tk.Frame(window)
frame_neuroni.pack(pady=20)

tk.Label(window, text="Operația matematică:").pack()
combo_operatii = ttk.Combobox(window, values=["Sumă", "Produs", "Min", "Max"])
combo_operatii.current(0)
combo_operatii.pack()

tk.Label(window, text="Funcția de activare:").pack()
combo_activare = ttk.Combobox(window, values=["Sigmoid", "Tanh", "ReLU", "Linear", "Step"])
combo_activare.current(0)
combo_activare.pack()


buton_calculeaza_intermediar = tk.Button(window, text="Calculează Intermediar", command=calcul_functii)
buton_calculeaza_intermediar.pack(pady=5)


buton_calculeaza = tk.Button(window, text="Calculează", command=calcul_functii_activare)
buton_calculeaza.pack(pady=20)


label_rezultat_intermediar = tk.Label(window, text="Rezultat intermediar: ")
label_rezultat_intermediar.pack()


label_rezultat = tk.Label(window, text="Rezultat final: ")
label_rezultat.pack()

label_binar = tk.Label(window,text="Binar sau Real")
label_binar.pack()

window.mainloop()