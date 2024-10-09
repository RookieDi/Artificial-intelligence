import tkinter as tk
from tkinter import W, Checkbutton, IntVar, ttk
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math





inputs = []
weights = []



intrari_valori = {}  
num_input_neurons = 0  
num_middle_neurons=0



def open_neuron_nero(neuron_type, neuron_index):
    new_window = tk.Toplevel(main_Window)
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
        all_spinbox = ttk.Spinbox(frame, from_=0.0, to=5.0, increment=0.01, width=8)
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
            spinbox = ttk.Spinbox(frame, from_=0.0, to=5.0, increment=0.01, width=8)
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
    global hidden_total_value
    global input_value
    global weight_value
    for label, field in fields.items():
        value = field.get()
        intrari_valori[(neuron_index, neuron_type, label)] = value

    if neuron_type == "Hidden":
        total_input_value = 0.0
        for i in range(num_input_neurons):
            input_value = float(intrari_valori.get((i, 'Input', 'GIN'), 0.0))
            weight_value = float(spinboxes[i].get())
            total_input_value += input_value + weight_value  

       
        fields["GIN"].config(state='normal')
        fields["GIN"].delete(0, tk.END)
        fields["GIN"].insert(0, str(total_input_value))
        fields["GIN"].config(state='readonly')

        intrari_valori[(neuron_index, neuron_type, 'GIN')] = str(total_input_value)

        
        hidden_total_value = total_input_value
   
        update_output_neurons(hidden_total_value)
        return  hidden_total_value
       
        

    
    elif neuron_type == "Output":
        total_input_value = 0.0
        for i in range(num_middle_neurons):
            input_value = float(intrari_valori.get((i, 'Hidden', 'GIN'), 0.0))
            weight_value = float(spinboxes[i].get())
            total_input_value += input_value + weight_value  

        
        new_output_value = float(fields["GIN"].get()) if 'GIN' in fields else 0.0

        
        total_input_value += new_output_value

        print(f"Final value after adding output neuron value: {total_input_value} (hidden sum + output neuron)")

       
        fields["GIN"].config(state='normal')
        fields["GIN"].delete(0, tk.END)
        fields["GIN"].insert(0, str(total_input_value))
        fields["GIN"].config(state='readonly')

        intrari_valori[(neuron_index, neuron_type, 'GIN')] = str(total_input_value)
        return  intrari_valori

def calculate_total_gin(layer_type):
    total_gin_value = 0.0

    if layer_type == 'hidden':
        num_neurons = num_middle_neurons  
    elif layer_type == 'output':
        num_neurons = num_output_neurons  
    else:
        raise ValueError("Invalid layer type")

    for neuron_index in range(num_neurons):
        if layer_type == 'hidden':
            gin_value = intrari_valori.get((neuron_index, 'Hidden', 'GIN'), 0.0)  
            total_gin_value += float(gin_value)  
        elif layer_type == 'output':
            
            gin_value = activated_value
            print(activated_value)
            total_gin_value += float(gin_value)

    return total_gin_value



def update_output_neurons(hidden_total_value):
    global activated_value
    for output_neuron_index in range(num_middle_neurons):
       
        total_input_value = hidden_total_value  

        
        new_output_value = float(intrari_valori.get((output_neuron_index, 'Output', 'GIN'), 0.0))
        
       
        total_input_value += new_output_value

        
        for i in range(num_input_neurons):  
            input_value = float(intrari_valori.get((i, 'Output', 'GIN'), 0.0))
            weight_value = float(intrari_valori.get((i, 'Output', 'weight'), 0.0)) 
            
            
            total_input_value += input_value + weight_value  
            
        total_input_value += activated_value   
        
        intrari_valori[(output_neuron_index, 'Output', 'GIN')] = str(total_input_value)

        
       



     





def update_all_values(value, fields):
    for field in fields.values():
        field.config(state='normal')
        field.delete(0, tk.END)
        field.insert(0, value)
        field.config(state='readonly') 


def save_input_spinbox_value(value, neuron_index):
    intrari_valori[(neuron_index, 'input', 'GIN')] = value



def save_weight_value(value, neuron_index, input_neuron_index, neuron_type):
    intrari_valori[(input_neuron_index, neuron_type, 'weight')] = value

def desenare(canvas, nr_input_neurons, hidden_neurons, nr_hidden_neurons):
    global num_input_neurons  
    global num_middle_neurons
    global num_output_neurons
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
        canvas.tag_bind(f'input_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron_nero("Input", n))
        num_input_neurons = nr_input_neurons

   


    hidden_neurons_coordinates = []
    for i in range(hidden_neurons):
        x = (canvas_width) / (hidden_neurons + 1) * (i + 1)
        y = canvas_height / 2
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'hidden_neuron_{i}')
        hidden_neurons_coordinates.append((x, y))
        canvas.tag_bind(f'hidden_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron_nero("Hidden", n))
        num_middle_neurons= hidden_neurons

    output_neurons_coordinates = []
    for i in range(nr_hidden_neurons):
        x = (canvas_width) / (nr_hidden_neurons + 1) * (i + 1)
        y = (3 * canvas_height) / 4
        canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'output_neuron_{i}')
        output_neurons_coordinates.append((x, y))
        canvas.tag_bind(f'output_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron_nero("Output", n))
        num_output_neurons=nr_hidden_neurons


    for input_coord in neurons_coordinates:
        for hidden_coord in hidden_neurons_coordinates:
            canvas.create_line(input_coord[0], input_coord[1], hidden_coord[0], hidden_coord[1])

    for hidden_coord in hidden_neurons_coordinates:
        for output_coord in output_neurons_coordinates:
            canvas.create_line(hidden_coord[0], hidden_coord[1], output_coord[0], output_coord[1])
def update_desen(canvas, input_neurons, hidden_neurons, output_neurons):
    canvas.update_idletasks()
    desenare(canvas, input_neurons, hidden_neurons, output_neurons)




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



def activari(value, function_name):
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


def agregari(values, function_name):
    if function_name == 'Sum':
        return suma(values)
    elif function_name == 'Product':
        return produs(values)
    elif function_name == 'Min':
        return minim(values)
    elif function_name == 'Max':
        return maxim(values)
    return suma(values)  

activare_functii = ['Sigmoid', 'Step', 'ReLU', 'Tanh', 'Linear', 'Signum']
functii = ['Sum', 'Product', 'Min', 'Max']

def functii_activare(neuron_type):
    global activated_value
    new_window = tk.Toplevel(main_Window)
    new_window.title(f"{neuron_type} Neuron Settings")

    frame_neuron = tk.Frame(new_window, bg='white')
    frame_neuron.pack(pady=5)

    label_activation = tk.Label(new_window, text=f"Activation {neuron_type}:", font=("Arial", 12))
    label_activation.pack(pady=10)

    activation_combo = ttk.Combobox(new_window, values=activare_functii, width=15)
    activation_combo.set(activare_functii[0])  
    activation_combo.pack(pady=10)

    label_aggregation = tk.Label(new_window, text=f"Agregations{neuron_type}:", font=("Arial", 12))
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

 
    total_gin_value = calculate_total_gin(neuron_type)
    print(f"Total GIN value for {neuron_type} neurons: {total_gin_value}")
    

    aggregation_function = aggregation_combo.get()
    aggregated_value = agregari([total_gin_value], aggregation_function)  
    def upd():
        global activated_value 
        activation_function = activation_combo.get()
        activated_value = activari(aggregated_value, activation_function)
        label_rezultat.config(text=f"Rezultat final: {activated_value:.2f}")
        print(activated_value)
        update_output_neurons(activated_value)
        return activated_value

    buton_update = tk.Button(new_window, text="Update", command=upd)
    buton_update.pack(pady=10)
    
   
main_Window = tk.Tk()
main_Window.title("Rețea Neuronală")
main_Window.state('zoomed')
main_Window.configure(bg='lightgrey')

frame_neuroni = tk.Frame(main_Window, bg='white', bd=2, relief=tk.SUNKEN)
frame_neuroni.pack(padx=20, pady=20, fill=tk.X)

for col in range(7):
    frame_neuroni.grid_columnconfigure(col, weight=1)

label_select_neurons = tk.Label(frame_neuroni, text="Număr Neuroni de Intrare:", font=("Arial", 12), bg='white')
label_select_neurons.grid(row=0, column=0, padx=10, pady=10)  

nr_input_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5, state="readonly")
nr_input_neurons.set(1)
nr_input_neurons.grid(row=0, column=1, padx=10, pady=10) 

label_select_hidden = tk.Label(frame_neuroni, text="Număr Neuroni Ascunși:", font=("Arial", 12), bg='white')
label_select_hidden.grid(row=0, column=2, padx=10, pady=10)  

nr_hidden_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5, state="readonly")
nr_hidden_neurons.set(1)
nr_hidden_neurons.grid(row=0, column=3, padx=10, pady=10) 

hidden_activare = tk.Button(frame_neuroni, text="Activare", command=lambda: functii_activare('hidden'), bg='lightblue', font=("Arial", 10))
hidden_activare.grid(row=1, column=2, padx=10, pady=10)  

label_select_output = tk.Label(frame_neuroni, text="Număr Neuroni de Ieșire:", font=("Arial", 12), bg='white')
label_select_output.grid(row=0, column=4, padx=10, pady=10)  

nr_output_neurons = ttk.Combobox(frame_neuroni, values=[i for i in range(1, 10)], width=5, state="readonly")
nr_output_neurons.set(1)
nr_output_neurons.grid(row=0, column=5, padx=10, pady=10) 

output_activare = tk.Button(frame_neuroni, text="Activare", command=lambda: functii_activare('output'), bg='lightblue', font=("Arial", 10))
output_activare.grid(row=1, column=5, padx=10, pady=10)  

frame_network = tk.Frame(main_Window, bg='white')
frame_network.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
canvas = tk.Canvas(frame_network, bg='lightgrey')
canvas.pack(fill=tk.BOTH, expand=True)
draw_button = tk.Button(main_Window, text="Actualizare Neuroni", command=lambda: desenare(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())), bg='green', fg='white', font=("Arial", 12))
draw_button.pack(pady=20)
main_Window.bind("<Configure>", lambda event: update_desen(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))

main_Window.mainloop()
