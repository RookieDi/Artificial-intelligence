import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math



intrare = []
greutate = []

def sigmoid(x, tetha, a):
    return 1 / (1 + math.exp(-(x - tetha) / a))

def treapta(x, tetha,a):
    if (x -tetha)>= a:
        return 1
    else:
        return 0

def relu(x):
    return max(0, x)

def tanh(x, tetha, a):
    return math.tanh((x - tetha) / a)

def linear(x, tetha, a):
    return (x - tetha) / a

def signum(x, tetha,a):
    if (x -tetha)> a:
        return 1
    elif (x-tetha) < a:
        return -1
    else:
        return 0


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

def actualizeaza_neuroni():
    new_window = tk.Toplevel(window)
    new_window.title("Intrări Neuroni")
    numar_neuroni = int(nr_neuroni.get())
    for i in range(numar_neuroni):
        frame_neuron = tk.Frame(new_window, bg='white')
        frame_neuron.pack(pady=5)
        tk.Label(frame_neuron, text=f"Intrare:{i+1}", bg='powderblue').pack(side=tk.LEFT, padx=5)
        entry_input = tk.Entry(frame_neuron, width=10)
        entry_input.pack(side=tk.LEFT, padx=5)
        intrare.append(entry_input)
        tk.Label(frame_neuron, text=f"greutate:{i+1}", bg='powderblue').pack(side=tk.LEFT, padx=5)
        entry_weight = tk.Entry(frame_neuron, width=10)
        entry_weight.pack(side=tk.LEFT, padx=5)
        greutate.append(entry_weight)


def calcul_functii():
    valori = []
    try:
        for i in range(len(intrare)):
            intrare_calcul = float(intrare[i].get())
            greutate_calcul = float(greutate[i].get())
            valori.append(intrare_calcul * greutate_calcul)

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
        teta = float(text_teta.get())
        alpha = float(text_alpha.get())
        activare = combo_activare.get()
        if activare == 'Sigmoid':
            rezultat_final = sigmoid(rezultat_intermediar, teta, alpha)
        elif activare == 'Tanh':
            rezultat_final = tanh(rezultat_intermediar, teta, alpha)
        elif activare == 'ReLU':
            rezultat_final = relu(rezultat_intermediar)  
        elif activare == 'Linear':
            rezultat_final = linear(rezultat_intermediar, teta, alpha)
        elif activare == 'Step':
            rezultat_final = treapta(rezultat_intermediar, teta,alpha)
        elif activare == 'Signum':
            rezultat_final = signum(rezultat_intermediar, teta, alpha)
        label_rezultat.config(text=f"Rezultat final: {rezultat_final:.4f}")
        return rezultat_final


def calcul_binar():
        rezultat_binar = calcul_functii_activare()
        if rezultat_binar is not None:
            activare = binar_real_combobox.get()
            func_activare = combo_activare.get()
            if func_activare in ['Step', 'Signum']:
                if activare == 'Binar':
                    if rezultat_binar >= 0.5:
                        label_binar.config(text="Binar: 1")
                    else:
                        label_binar.config(text="Binar: 0")
                elif activare == 'Real':
                    label_binar.config(text=f"Real: {rezultat_binar:.5f}")
            elif func_activare in ['Sigmoid', 'Tanh', 'ReLU', 'Linear']: 
                if activare == 'Binar':
                    if rezultat_binar >= 0.5:
                        label_binar.config(text="Binar: 1")
                    else:
                        label_binar.config(text="Binar: 0")
                elif activare == 'Real':
                    label_binar.config(text=f"Real: {rezultat_binar:.5f}")
            else:
                label_binar.config(text="Funcția selectată nu este suportată.")
   
def grafic():
    
    rezultat_intermediar = calcul_functii_activare()  
    if rezultat_intermediar is None:
        return
    tetha = float(text_teta.get())
    alpha = float(text_alpha.get())
    activare = combo_activare.get()

    functii_activare = {
        'Sigmoid': sigmoid,
        'Tanh': tanh,
        'ReLU': relu,
        'Linear': linear,
        'Step': treapta,
        'Signum': signum
    }

    functie = functii_activare.get(activare) 
    if functie is None:
        return
    x = np.linspace(-10, 10, 400)
    y_grafic = []  
    for val in x:
        if activare in ['Sigmoid', 'Tanh', 'Linear', 'Signum']:
            y_grafic.append(functie(val + rezultat_intermediar, tetha, alpha))
        elif activare == 'ReLU':
            y_grafic.append(functie(val + rezultat_intermediar))
        elif activare == 'Step':
            y_grafic.append(functie(val + rezultat_intermediar, tetha, alpha))

    for widget in frame_poza.winfo_children():
        widget.destroy()

    plt.figure(figsize=(8, 6))
    
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

    plt.plot(x, y_grafic, label=f"Funcția: {activare} (cu offset: {rezultat_intermediar:.4f})")
    plt.xlabel('x - axă')
    plt.ylabel('y - axă')
    plt.title(f'Graficul funcției de activare: {activare}')
    plt.legend()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_poza)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)




window = tk.Tk()
window.title("Rețea Neuronală Simplă")
window.state('zoomed')
window.configure(bg='lightgray')

frame_optiuni = tk.Frame(window, bg='white', bd=5, relief=tk.GROOVE)
frame_optiuni.grid(row=0, column=0, sticky="nsew")

frame_poza = tk.Frame(window, bd=5, relief=tk.SUNKEN)
frame_poza.grid(row=0, column=1, sticky="nsew")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=2)


tk.Label(frame_optiuni, text="Număr de intrari:",bg='beige', font=("Arial", 12)).pack(pady=10)
nr_neuroni = ttk.Combobox(frame_optiuni, values=[i for i in range(1, 11)], width=5)
nr_neuroni.set(1)
nr_neuroni.pack()
nr_neuroni.bind("<<ComboboxSelected>>", lambda event: actualizeaza_neuroni())

tk.Label(frame_optiuni, text="Calcul Intrari:", bg='white', font=("Arial", 12)).pack(pady=10)
combo_operatii = ttk.Combobox(frame_optiuni, values=["Sumă", "Produs", "Min", "Max"])
combo_operatii.current(0)
combo_operatii.pack()


tk.Label(frame_optiuni, text="Funcția de activare:", bg='white', font=("Arial", 12)).pack(pady=10)
combo_activare = ttk.Combobox(frame_optiuni, values=["Sigmoid", "Tanh", "ReLU", "Linear", "Step","Signum"])
combo_activare.current(0)
combo_activare.pack()


buton_calculeaza_intermediar = tk.Button(frame_optiuni, text="Calculează Intermediar", command=calcul_functii, bg="lightblue", font=("Arial", 12))
buton_calculeaza_intermediar.pack(pady=5)

buton_calculeaza = tk.Button(frame_optiuni, text="Calculează Final", command=calcul_functii_activare, bg="lightgreen", font=("Arial", 12))
buton_calculeaza.pack(pady=20)


label_rezultat_intermediar = tk.Label(frame_optiuni, text="Rezultat intermediar: ", bg='white', font=("Arial", 12))
label_rezultat_intermediar.pack(pady=10)

label_rezultat = tk.Label(frame_optiuni, text="Rezultat final: ", bg='white', font=("Arial", 12))
label_rezultat.pack(pady=10)

binar_real_combobox=ttk.Combobox(frame_optiuni,values=["Binar","Real"])
binar_real_combobox.current(0)
binar_real_combobox.pack()
binar_real_combobox.bind("<<ComboboxSelected>>",lambda event: calcul_binar())

label_binar = tk.Label(frame_optiuni, text="Binar sau Real:", bg='white', font=("Arial", 12))
label_binar.pack(pady=10)

btn = tk.Button(frame_optiuni,command=grafic,text="Grafic")
btn.pack(pady=20)


tk.Label(frame_optiuni, text="Valoare Θ:", bg='white', font=("Arial", 12)).pack(pady=5)
text_teta = tk.Entry(frame_optiuni, width=10)
text_teta.pack(pady=5)

tk.Label(frame_optiuni, text="Valoare α:", bg='white', font=("Arial", 12)).pack(pady=5)
text_alpha = tk.Entry(frame_optiuni, width=10)
text_alpha.pack(pady=5)




window.mainloop()
