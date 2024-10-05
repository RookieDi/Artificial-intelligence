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






intrari_valori = {}  
num_input_neurons = 0  
num_middle_neurons=0



def open_neuron(neuron_type, neuron_index):
    new_window = tk.Toplevel(window)
    new_window.title(f"{neuron_type} Neuron {neuron_index} Settings")

    frame = tk.Frame(new_window, bg="black")
    frame.pack(padx=20, pady=20)

    labels = ["GIN", "ACT", "OUT"]
    fields = {}

    for i, label_text in enumerate(labels):
        tk.Label(frame, text=label_text, fg="cyan", bg="black", font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=5)
        field = tk.Entry(frame, width=10, justify='center')
        field.grid(row=i, column=1, padx=5, pady=5)

        if label_text == "GIN":
            field_value = intrari_valori.get((neuron_index, neuron_type, 'GIN'), "0.00")
        elif neuron_type in ["Hidden", "Output"]:
            field_value = "1.00"
        else:
            field_value = "0.00"

        print(f"Setting initial value for {label_text} of neuron {neuron_index}: {field_value}")
        field.insert(0, field_value)
        field.config(state='normal' if neuron_type in ["Hidden", "Output"] else 'readonly')
        fields[label_text] = field

    if neuron_type == "Input":
        tk.Label(frame, text="Set All:", fg="cyan", bg="black", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        all_spinbox = ttk.Spinbox(frame, from_=0.0, to=1.0, increment=0.01, width=8)
        all_spinbox.grid(row=3, column=1, padx=5, pady=5)
        all_spinbox.bind('<Return>', lambda event: update_all_values(all_spinbox.get(), fields))
        all_spinbox.bind('<ButtonRelease-1>', lambda event: update_all_values(all_spinbox.get(), fields))
        all_spinbox.bind("<<Increment>>", lambda event: save_input_spinbox_value(all_spinbox.get(), neuron_index))
    elif neuron_type in ["Hidden", "Output"]:
        tk.Label(frame, text="Weight:", fg="cyan", bg="black", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)

        nr_input_neurons = num_input_neurons if neuron_type == "Hidden" else num_middle_neurons

        print(f"Number of input neurons for {neuron_type}: {nr_input_neurons}")

        if nr_input_neurons == 0:
            print("Warning: No input neurons defined!")

        spinboxes = []
        for i in range(nr_input_neurons):
            spinbox = ttk.Spinbox(frame, from_=0.0, to=1.0, increment=0.01, width=8)
            spinbox.grid(row=3, column=i + 1, padx=5, pady=5)

            spinbox_value = intrari_valori.get((i, 'hidden' if neuron_type == 'Output' else 'input', 'GIN'), "0.00")
            print(f"Setting initial value for spinbox {i}: {spinbox_value}")
            spinbox.set(spinbox_value)

            spinbox.bind("<<Increment>>", lambda event, idx=i: save_weight_value(spinbox.get(), neuron_index, idx, neuron_type))

            tk.Label(frame, text=f"w{i + 1}", fg="cyan", bg="black", font=("Arial", 12)).grid(row=4, column=i + 1, padx=5, pady=5)

            spinboxes.append(spinbox)

    update_button = tk.Button(frame, text="Update", fg="cyan", bg="black", activebackground="cyan", activeforeground="black", command=lambda: save_input_values(fields, neuron_index, neuron_type, spinboxes))
    update_button.grid(row=5, columnspan=2, pady=10)


def save_input_values(fields, neuron_index, neuron_type, spinboxes):
    for label, field in fields.items():
        value = field.get()
        intrari_valori[(neuron_index, neuron_type, label)] = value
        print(f"Saved value for neuron {neuron_index} - {label}: {value}")

    if neuron_type == "Hidden":
        total_input_value = 0.0
        for i in range(num_input_neurons):
            input_value = float(intrari_valori.get((i, 'input', 'GIN'), 0.0))
            weight_value = float(spinboxes[i].get())
            total_input_value += input_value + weight_value  
            print(f"Input neuron {i} GIN: {input_value} * weight {weight_value} = {input_value * weight_value}")

       
        fields["GIN"].config(state='normal')
        fields["GIN"].delete(0, tk.END)
        fields["GIN"].insert(0, str(total_input_value))
        fields["GIN"].config(state='readonly')

        intrari_valori[(neuron_index, neuron_type, 'GIN')] = str(total_input_value)
        print(f"Updated GIN for hidden neuron {neuron_index}: {total_input_value}")

        
        hidden_total_value = total_input_value
        
       
        update_output_neurons(hidden_total_value)

    
    elif neuron_type == "Output":
        total_input_value = 0.0
        for i in range(num_middle_neurons):
            input_value = float(intrari_valori.get((i, 'hidden', 'GIN'), 0.0))
            weight_value = float(spinboxes[i].get())
            total_input_value += input_value + weight_value  
            print(f"Hidden neuron {i} GIN: {input_value} * weight {weight_value} = {input_value * weight_value}")

        
        new_output_value = float(fields["GIN"].get()) if 'GIN' in fields else 0.0
        print(f"Retrieved output neuron value: {new_output_value}")

        
        total_input_value += new_output_value

        print(f"Final value after adding output neuron value: {total_input_value} (hidden sum + output neuron)")

       
        fields["GIN"].config(state='normal')
        fields["GIN"].delete(0, tk.END)
        fields["GIN"].insert(0, str(total_input_value))
        fields["GIN"].config(state='readonly')

        intrari_valori[(neuron_index, neuron_type, 'GIN')] = str(total_input_value)
        print(f"Updated GIN for output neuron {neuron_index}: {total_input_value}")


def update_output_neurons(hidden_total_value):
    for output_neuron_index in range(num_middle_neurons):
        total_input_value = hidden_total_value  
        print(f"Starting total input value for output neuron {output_neuron_index}: {total_input_value}")

        
        for i in range(num_middle_neurons):
            input_value = float(intrari_valori.get((i, 'hidden', 'GIN'), 0.0))
            weight_value = float(intrari_valori.get((i, 'hidden', 'weight'), 1.0))
            total_input_value += input_value + weight_value 
            print(f"Hidden neuron {i} GIN: {input_value} * weight {weight_value} = {input_value * weight_value}")

        new_output_value = float(intrari_valori.get((output_neuron_index, 'output', 'GIN'), 0.0))
        print(f"Additional value from output neuron itself: {new_output_value}")

        total_input_value += new_output_value

        
        intrari_valori[(output_neuron_index, 'output', 'GIN')] = str(total_input_value)
        print(f"Updated GIN for output neuron {output_neuron_index}: {total_input_value}")



     





def update_all_values(value, fields):
    for field in fields.values():
        field.config(state='normal')
        field.delete(0, tk.END)
        field.insert(0, value)
        field.config(state='readonly') 


def save_input_spinbox_value(value, neuron_index):
    intrari_valori[(neuron_index, 'input', 'GIN')] = value
    print(f"Saved input neuron value for neuron {neuron_index}: {value}")


def save_weight_value(value, neuron_index, input_neuron_index, neuron_type):
    intrari_valori[(input_neuron_index, neuron_type, 'weight')] = value
    print(f"Saved weight for {neuron_type} neuron {neuron_index} from input neuron {input_neuron_index}: {value}")








def draw_neurons(canvas, nr_input_neurons, hidden_neurons, nr_hidden_neurons):
    global num_input_neurons  
    global num_middle_neurons
    canvas.delete("all")
    neuron_radius = 30
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    neurons_coordinates = []
  

    for i in range(nr_input_neurons):
        x = (canvas_width) / (nr_input_neurons + 1) * (i + 1)
        y = canvas_height / 4
        
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'input_neuron_{i}')
        neurons_coordinates.append((x, y))
        canvas.tag_bind(f'input_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron("Input", n))
        num_input_neurons = nr_input_neurons

   


    hidden_neurons_coordinates = []
    for i in range(hidden_neurons):
        x = (canvas_width) / (hidden_neurons + 1) * (i + 1)
        y = canvas_height / 2
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'hidden_neuron_{i}')
        hidden_neurons_coordinates.append((x, y))
        canvas.tag_bind(f'hidden_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron("Hidden", n))
        num_middle_neurons= hidden_neurons

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

import math

# Funcțiile de activare fără parametrii tetha și a
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def treapta(x):
    return 1 if x >= 0 else 0

def relu(x):
    return max(0, x)

def tanh(x):
    return math.tanh(x)

def linear(x):
    return x

def signum(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


# Funcțiile de agregare
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


# Funcția care aplică funcția de activare selectată
def apply_activation_function(value, function_name):
    if function_name == 'Sigmoid':
        return sigmoid(value)
    elif function_name == 'Tanh':
        return tanh(value)
    elif function_name == 'ReLU':
        return relu(value)
    elif function_name == 'Treapta':
        return treapta(value)
    elif function_name == 'Linear':
        return linear(value)
    elif function_name == 'Signum':
        return signum(value)
    return value


# Funcția care aplică funcția de agregare selectată
def apply_aggregation_function(values, function_name):
    if function_name == 'Sum':
        return suma(values)
    elif function_name == 'Product':
        return produs(values)
    elif function_name == 'Min':
        return minim(values)
    elif function_name == 'Max':
        return maxim(values)
    return suma(values)  # Default aggregation


# Fereastră pentru setarea funcțiilor de activare și agregare
def functii_activare(neuron_type):
    new_window = tk.Toplevel(main_Window)
    new_window.title(f"{neuron_type} Neuron Settings")

    frame_neuron = tk.Frame(new_window, bg='white')
    frame_neuron.pack(pady=5)

    label_activation = tk.Label(new_window, text=f"Activation Function for {neuron_type}:", font=("Arial", 12))
    label_activation.pack(pady=10)

    activation_combo = ttk.Combobox(new_window, values=activare_functii, width=15)
    activation_combo.set(activare_functii[0])  
    activation_combo.pack(pady=10)

    label_aggregation = tk.Label(new_window, text=f"Aggregation Function for {neuron_type}:", font=("Arial", 12))
    label_aggregation.pack(pady=10)

    aggregation_combo = ttk.Combobox(new_window, values=functii, width=15)
    aggregation_combo.set(functii[0])  
    aggregation_combo.pack(pady=10)

    label_rezultat = tk.Label(new_window, text="Rezultat final: ", bg='white', font=("Arial", 12))
    label_rezultat.pack(pady=10)

    global real, binar
    real = IntVar()
    binar = IntVar()

    def toggle_checkbutton(selected):
        if selected == "real":
            binar.set(0)
        elif selected == "binar":
            real.set(0)

    Checkbutton(frame_neuron, text="Real", variable=real, command=lambda: toggle_checkbutton("real")).grid(row=0, sticky=W)
    Checkbutton(frame_neuron, text="Binar", variable=binar, command=lambda: toggle_checkbutton("binar")).grid(row=1, sticky=W)

   
    neuron_index = 0  
    gin_value = float(intrari_valori.get((neuron_index, neuron_type, 'GIN'), 0.0))

    
    aggregation_function = aggregation_combo.get()
    aggregated_value = apply_aggregation_function([gin_value], aggregation_function)  

    
    activation_function = activation_combo.get()
    activated_value = apply_activation_function(aggregated_value, activation_function)

    
    label_rezultat.config(text=f"Rezultat final: {activated_value:.2f}")


        
            
      


     

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


frame_neuroni = tk.Frame(main_Window, bg='white')
frame_neuroni.pack(fill=tk.BOTH, expand=True)
frame_neuroni.grid_columnconfigure(0, weight=1)
frame_neuroni.grid_columnconfigure(1, weight=1)
frame_neuroni.grid_columnconfigure(2, weight=1)
frame_neuroni.grid_columnconfigure(3, weight=1)
frame_neuroni.grid_columnconfigure(4, weight=1)
frame_neuroni.grid_columnconfigure(5, weight=1)
frame_neuroni.grid_columnconfigure(6, weight=1)


label_select_neurons = tk.Label(frame_neuroni, text="Number of Input Neurons:", font=("Arial", 16), bg='white')
label_select_neurons.grid(row=0, column=0, padx=5, pady=10)  

nr_input_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5)
nr_input_neurons.set(1)
nr_input_neurons.grid(row=0, column=1, padx=0, pady=10) 


label_select_hidden = tk.Label(frame_neuroni, text="Number of Hidden Neurons:", font=("Arial", 16), bg='white')
label_select_hidden.grid(row=0, column=2, padx=0, pady=10)  

nr_hidden_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5)
nr_hidden_neurons.set(1)
nr_hidden_neurons.grid(row=0, column=3, padx=0, pady=10) 

hidden_activare = tk.Button(frame_neuroni, text="Activare", command=lambda: functii_activare('hidden'))
hidden_activare.grid(row=1, column=2, padx=10, pady=10)  


label_select_output = tk.Label(frame_neuroni, text="Number of Output Neurons:", font=("Arial", 16), bg='white')
label_select_output.grid(row=0, column=5, padx=5, pady=10)  

nr_output_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5)
nr_output_neurons.set(1)
nr_output_neurons.grid(row=0, column=6, padx=0, pady=10) 
hidden_activare = tk.Button(frame_neuroni, text="Activare", command=lambda: functii_activare('output'))
hidden_activare.grid(row=1, column=5, padx=10, pady=10)  




frame_network = tk.Frame(main_Window, bg='white')
frame_network.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_network, bg='lightgrey')
canvas.pack(fill=tk.BOTH, expand=True)


draw_button = tk.Button(main_Window, text="Update Neurons", command=lambda: draw_neurons(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))
draw_button.pack(pady=20)


main_Window.bind("<Configure>", lambda event: update_canvas(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))

main_Window.mainloop()
