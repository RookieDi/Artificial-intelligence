import tkinter as tk
from tkinter import W, Checkbutton, IntVar, ttk
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

def creare_campuri():
    new_window = tk.Toplevel(window)
    new_window.title("Intrări Neuroni")
    numar_neuroni = int(nr_neuroni.get())

    def creare_cmp_recursiv(index):
        if index >= numar_neuroni:
            return  

        frame_neuron = tk.Frame(new_window, bg='white')
        frame_neuron.pack(pady=5)

        tk.Label(frame_neuron, text=f"Intrare: {index + 1}", bg='powderblue').pack(side=tk.LEFT, padx=5)
        entry_input = tk.Entry(frame_neuron, width=10)
        entry_input.pack(side=tk.LEFT, padx=5)
        intrare.append(entry_input)

        tk.Label(frame_neuron, text=f"greutate: {index + 1}", bg='powderblue').pack(side=tk.LEFT, padx=5)
        entry_weight = tk.Entry(frame_neuron, width=10)
        entry_weight.pack(side=tk.LEFT, padx=5)
        greutate.append(entry_weight)

        creare_cmp_recursiv(index + 1)


    creare_cmp_recursiv(0)



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

inputs = []
weights = []
activare_functii = ['Sigmoid', 'Step', 'ReLU', 'Tanh', 'Linear', 'Signum']
functii = ['Sum', 'Product', 'Min', 'Max']





def create_input_fields(neuron_type, neuron_index, num_inputs):
    new_window = tk.Toplevel(window)
    new_window.title(f"Neuron {neuron_type} {neuron_index} Settings")
    
    
    inputs.clear()
    weights.clear()

  
    def create_fields(index):
        frame_neuron = tk.Frame(new_window, bg='white')
        frame_neuron.pack(pady=5)

        tk.Label(frame_neuron, text=f"Input {index + 1}: ", bg='powderblue').pack(side=tk.LEFT, padx=5)
        entry_input = tk.Entry(frame_neuron, width=10)
        entry_input.pack(side=tk.LEFT, padx=5)
        inputs.append(entry_input)

        tk.Label(frame_neuron, text=f"Weight {index + 1}: ", bg='powderblue').pack(side=tk.LEFT, padx=5)
        entry_weight = tk.Entry(frame_neuron, width=10)
        entry_weight.pack(side=tk.LEFT, padx=5)
        weights.append(entry_weight)

   
    label_num_inputs = tk.Label(new_window, text="Number of Inputs/Weights:", font=("Arial", 12))
    label_num_inputs.pack(pady=10)
    num_inputs_combo = tk.Label(new_window, width=5)
    num_inputs_combo.pack(pady=10)

   
    frame_theta_a = tk.Frame(new_window, bg='white')
    frame_theta_a.pack(pady=10)

    tk.Label(frame_theta_a, text="θ (Theta):", bg='powderblue').pack(side=tk.LEFT, padx=5)
    entry_theta = tk.Entry(frame_theta_a, width=5)
    entry_theta.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_theta_a, text="a:", bg='powderblue').pack(side=tk.LEFT, padx=5)
    entry_a = tk.Entry(frame_theta_a, width=5)
    entry_a.pack(side=tk.LEFT, padx=5)

   
    def update_fields():
      
        for widget in new_window.winfo_children():
            if isinstance(widget, tk.Frame) and widget != frame_theta_a:
                widget.destroy()

        inputs.clear() 
        weights.clear() 
        selected_num_inputs = int(num_inputs_combo.get())
        for i in range(selected_num_inputs):
            create_fields(i)

    num_inputs_combo.bind("<<ComboboxSelected>>", lambda event: update_fields())
    update_fields()  



    
    label_result = tk.Label(new_window, text="Final Result:", font=("Arial", 14), bg='white')
    label_result.pack(pady=20)

    result_value = tk.Label(new_window, text="", font=("Arial", 12), bg='white', fg='blue')
    result_value.pack()
        


intrari_valori = {}    
comboboxuri_intrari = {}

def open_neuron(neuron_type, neuron_index):
    new_window = tk.Toplevel(window)
    new_window.title(f"{neuron_type} Neuron {neuron_index}")

    if neuron_type == "Input":
        tk.Label(new_window, text=f"Valoare selectată pentru Neuronul de intrare {neuron_index}:").pack(pady=10)
        valoare_selectata = intrari_valori.get(neuron_index, "Nicio valoare selectată")
        tk.Label(new_window, text=valoare_selectata).pack()
     
def save_input_value(event, neuron_index):
    valoare = comboboxuri_intrari[neuron_index].get()  
    intrari_valori[neuron_index] = valoare  
    print(f"Valoare salvată pentru neuronul de intrare {neuron_index}: {valoare}")



def draw_neurons(canvas, nr_input_neurons, hidden_neurons, nr_hidden_neurons):
    canvas.delete("all")
    neuron_radius = 30
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    neurons_coordinates = []
    comboboxuri_intrari.clear()
    
    for i in range(nr_input_neurons):
        x = (canvas_width) / (nr_input_neurons + 1) * (i + 1)
        y = canvas_height / 4
        
       
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'input_neuron_{i}')
        neurons_coordinates.append((x, y))
        label_valori = tk.Label(main_Window, text=f"Neuron {i}", bg="white")
        canvas.create_window(x, y + 30, window=label_valori)    
        canvas.tag_bind(f'input_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron("Input", n))

    hidden_neurons_coordinates = []
    for i in range(hidden_neurons):
        x = (canvas_width) / (hidden_neurons + 1) * (i + 1)
        y = canvas_height / 2
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'hidden_neuron_{i}')
        hidden_neurons_coordinates.append((x, y))
        canvas.tag_bind(f'hidden_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron("Hidden", n))

    output_neurons_coordinates = []
    for i in range(nr_hidden_neurons):
        x = (canvas_width) / (nr_hidden_neurons + 1) * (i + 1)
        y = (3 * canvas_height) / 4
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'output_neuron_{i}')
        output_neurons_coordinates.append((x, y))
        canvas.tag_bind(f'output_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron("Output", n))

    
    for input_coord in neurons_coordinates:
        for hidden_coord in hidden_neurons_coordinates:
            canvas.create_line(input_coord[0], input_coord[1], hidden_coord[0], hidden_coord[1])

    for hidden_coord in hidden_neurons_coordinates:
        for output_coord in output_neurons_coordinates:
            canvas.create_line(hidden_coord[0], hidden_coord[1], output_coord[0], output_coord[1])

def update_canvas(canvas, input_neurons, hidden_neurons, output_neurons):
    canvas.update_idletasks()
    draw_neurons(canvas, input_neurons, hidden_neurons, output_neurons)


def functii_activare():
      new_window = tk.Toplevel(main_Window)
      new_window.title("Neuron  Settings")
      frame_neuron = tk.Frame(new_window, bg='white')
      frame_neuron.pack(pady=5)
      label_activation = tk.Label(new_window, text="Activation Function:", font=("Arial", 12))
      label_activation.pack(pady=10)
      activation_combo = ttk.Combobox(new_window, values=activare_functii, width=15)
      activation_combo.set(activare_functii[0])  
      activation_combo.pack(pady=10)

   
      label_aggregation = tk.Label(new_window, text="Aggregation Function:", font=("Arial", 12))
      label_aggregation.pack(pady=10)
      aggregation_combo = ttk.Combobox(new_window, values=functii, width=15)
      aggregation_combo.set(functii[0]) 
      aggregation_combo.pack(pady=10)
      label_rezultat = tk.Label(new_window, text="Rezultat final: ", bg='white', font=("Arial", 12))
      label_rezultat.pack(pady=10)
      binar=IntVar()
      real=IntVar()
      Checkbutton(frame_neuron, text="real", variable=real).grid(row=0, sticky=W)
      Checkbutton(frame_neuron, text="binar", variable=binar).grid(row=1, sticky=W)
            
      


     

main_Window=tk.Tk()
main_Window.title("Reatea Neuronala")
main_Window.state('zoomed')
main_Window.configure(bg='grey')
window =  tk.Toplevel(main_Window)
window.title("vedem")
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
nr_neuroni = ttk.Combobox(frame_optiuni, values=[i for i in range(1, 20)], width=5)
nr_neuroni.set(1)
nr_neuroni.pack()
nr_neuroni.bind("<<ComboboxSelected>>", lambda event: creare_campuri())

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




tk.Label(frame_optiuni, text="Valoare Θ:", bg='white', font=("Arial", 12)).pack(pady=5)
text_teta = tk.Entry(frame_optiuni, width=10)
text_teta.pack(pady=5)

tk.Label(frame_optiuni, text="Valoare α:", bg='white', font=("Arial", 12)).pack(pady=5)
text_alpha = tk.Entry(frame_optiuni, width=10)
text_alpha.pack(pady=5)



#frame principal

frame_neuroni = tk.Frame(main_Window,bg='white')
frame_neuroni.pack(fill=tk.BOTH,expand=True)

label_select_neurons = tk.Label(frame_neuroni, text="Number of Input Neurons:", font=("Arial", 16), bg='white')
label_select_neurons.pack(pady=20)


nr_input_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5)
nr_input_neurons.set(1)
nr_input_neurons.pack(pady=10)

label_select_hidden = tk.Label(frame_neuroni, text="Number of Hidden Neurons:", font=("Arial", 16), bg='white')
label_select_hidden.pack(pady=20)
tk.Label(frame_optiuni, text="Funcția de activare:", bg='white', font=("Arial", 12)).pack(pady=10)


nr_hidden_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5)
nr_hidden_neurons.set(1)
nr_hidden_neurons.pack(pady=10)
hidden_activare = tk.Button(frame_neuroni,text="Activare",command=lambda: functii_activare())
hidden_activare.pack(padx=20)

label_select_output = tk.Label(frame_neuroni, text="Number of Output Neurons:", font=("Arial", 16), bg='white')
label_select_output.pack(pady=20)

nr_output_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5)
nr_output_neurons.set(1)
nr_output_neurons.pack(pady=10)


frame_network = tk.Frame(main_Window, bg='white')
frame_network.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_network, bg='lightgrey')
canvas.pack(fill=tk.BOTH, expand=True)


draw_button = tk.Button(main_Window, text="Update Neurons", command=lambda: draw_neurons(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))
draw_button.pack(pady=20)


main_Window.bind("<Configure>", lambda event: update_canvas(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))

main_Window.mainloop()
