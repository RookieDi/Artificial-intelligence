import tkinter as tk
from tkinter import ttk
import math


def sigmoid(x, theta, a):
    return 1 / (1 + math.exp(-(x - theta) / a))

def step(x, theta, a):
    return 1 if (x - theta) >= a else 0

def relu(x):
    return max(0, x)

def tanh(x, theta, a):
    return math.tanh((x - theta) / a)

def linear(x, theta, a):
    return (x - theta) / a

def signum(x, theta, a):
    if (x - theta) > a:
        return 1
    elif (x - theta) < a:
        return -1
    else:
        return 0


def sum_values(values):
    return sum(values)

def product(values):
    result = 1
    for val in values:
        result *= val
    return result

def min_value(values):
    return min(values)

def max_value(values):
    return max(values)


inputs = []
weights = []
activation_functions = ['Sigmoid', 'Step', 'ReLU', 'Tanh', 'Linear', 'Signum']
aggregation_functions = ['Sum', 'Product', 'Min', 'Max']

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
    num_inputs_combo = ttk.Combobox(new_window, values=[i for i in range(1, 11)], width=5)
    num_inputs_combo.set(num_inputs)  
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

    label_activation = tk.Label(new_window, text="Activation Function:", font=("Arial", 12))
    label_activation.pack(pady=10)
    activation_combo = ttk.Combobox(new_window, values=activation_functions, width=15)
    activation_combo.set(activation_functions[0])  
    activation_combo.pack(pady=10)

   
    label_aggregation = tk.Label(new_window, text="Aggregation Function:", font=("Arial", 12))
    label_aggregation.pack(pady=10)
    aggregation_combo = ttk.Combobox(new_window, values=aggregation_functions, width=15)
    aggregation_combo.set(aggregation_functions[0]) 
    aggregation_combo.pack(pady=10)

    
    label_result = tk.Label(new_window, text="Final Result:", font=("Arial", 14), bg='white')
    label_result.pack(pady=20)

    result_value = tk.Label(new_window, text="", font=("Arial", 12), bg='white', fg='blue')
    result_value.pack()

    def calculate_result():
        try:
            neuron_inputs = [float(inp.get()) for inp in inputs]
            neuron_weights = [float(weight.get()) for weight in weights]
            theta = float(entry_theta.get())
            a = float(entry_a.get())
            selected_activation = activation_combo.get()
            selected_aggregation = aggregation_combo.get()

            
            weighted_inputs = [neuron_inputs[i] * neuron_weights[i] for i in range(len(neuron_inputs))]

           
            if selected_aggregation == 'Sum':
                aggregated_value = sum_values(weighted_inputs)
            elif selected_aggregation == 'Product':
                aggregated_value = product(weighted_inputs)
            elif selected_aggregation == 'Min':
                aggregated_value = min_value(weighted_inputs)
            elif selected_aggregation == 'Max':
                aggregated_value = max_value(weighted_inputs)

         
            if selected_activation == 'Sigmoid':
                final_result = sigmoid(aggregated_value, theta, a)
            elif selected_activation == 'Step':
                final_result = step(aggregated_value, theta, a)
            elif selected_activation == 'ReLU':
                final_result = relu(aggregated_value)
            elif selected_activation == 'Tanh':
                final_result = tanh(aggregated_value, theta, a)
            elif selected_activation == 'Linear':
                final_result = linear(aggregated_value, theta, a)
            elif selected_activation == 'Signum':
                final_result = signum(aggregated_value, theta, a)

            
            result_value.config(text=f"{final_result:.4f}")

        except ValueError:
            result_value.config(text="Invalid input. Please enter valid numbers.")

    calculate_button = tk.Button(new_window, text="Calculate", command=calculate_result)
    calculate_button.pack(pady=20)

    save_button = tk.Button(new_window, text="Save", command=new_window.destroy)
    save_button.pack(pady=20)



def open_neuron_settings(neuron_type, neuron_index):
    num_inputs = 1 
    create_input_fields(neuron_type, neuron_index, num_inputs)


def draw_neurons(canvas, num_input_neurons, num_hidden_neurons, num_output_neurons):
    canvas.delete("all")

    neuron_radius = 30
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

   
    input_neuron_coords = []
    for i in range(num_input_neurons):
        x = (canvas_width / (num_input_neurons + 1)) * (i + 1)
        y = canvas_height / 4
        neuron = canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='blue', tags=f'input_neuron_{i}')
        input_neuron_coords.append((x, y))
        canvas.tag_bind(f'input_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron_settings("Input", n))

  
    hidden_neuron_coords = []
    for i in range(num_hidden_neurons):
        x = (canvas_width / (num_hidden_neurons + 1)) * (i + 1)
        y = canvas_height / 2
        neuron = canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='green', tags=f'hidden_neuron_{i}')
        hidden_neuron_coords.append((x, y))
        canvas.tag_bind(f'hidden_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron_settings("Hidden", n))

   
    output_neuron_coords = []
    for i in range(num_output_neurons):
        x = (canvas_width / (num_output_neurons + 1)) * (i + 1)
        y = (3 * canvas_height) / 4
        neuron = canvas.create_oval(x - neuron_radius, y - neuron_radius, x + neuron_radius, y + neuron_radius, fill='red', tags=f'output_neuron_{i}')
        output_neuron_coords.append((x, y))
        canvas.tag_bind(f'output_neuron_{i}', '<Button-1>', lambda event, n=i: open_neuron_settings("Output", n))

   
    for input_coord in input_neuron_coords:
        for hidden_coord in hidden_neuron_coords:
            canvas.create_line(input_coord[0], input_coord[1], hidden_coord[0], hidden_coord[1])

    for hidden_coord in hidden_neuron_coords:
        for output_coord in output_neuron_coords:
            canvas.create_line(hidden_coord[0], hidden_coord[1], output_coord[0], output_coord[1])


def update_canvas(canvas, num_input_neurons, num_hidden_neurons, num_output_neurons):
    canvas.update_idletasks()
    draw_neurons(canvas, num_input_neurons, num_hidden_neurons, num_output_neurons)


window = tk.Tk()
window.title("Neural Network")
window.geometry("1000x800")

frame_neurons = tk.Frame(window, bg='white')
frame_neurons.pack(fill=tk.BOTH, expand=True)


label_select_neurons = tk.Label(frame_neurons, text="Number of Input Neurons:", font=("Arial", 16), bg='white')
label_select_neurons.pack(pady=20)

nr_input_neurons = ttk.Combobox(frame_neurons, values=[i for i in range(1, 10)], width=5)
nr_input_neurons.set(1)
nr_input_neurons.pack(pady=10)

label_select_hidden = tk.Label(frame_neurons, text="Number of Hidden Neurons:", font=("Arial", 16), bg='white')
label_select_hidden.pack(pady=20)

nr_hidden_neurons = ttk.Combobox(frame_neurons, values=[i for i in range(1, 10)], width=5)
nr_hidden_neurons.set(1)
nr_hidden_neurons.pack(pady=10)

label_select_output = tk.Label(frame_neurons, text="Number of Output Neurons:", font=("Arial", 16), bg='white')
label_select_output.pack(pady=20)

nr_output_neurons = ttk.Combobox(frame_neurons, values=[i for i in range(1, 10)], width=5)
nr_output_neurons.set(1)
nr_output_neurons.pack(pady=10)

frame_network = tk.Frame(window, bg='white')
frame_network.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_network, bg='lightgrey')
canvas.pack(fill=tk.BOTH, expand=True)


draw_button = tk.Button(window, text="Draw Neurons", command=lambda: draw_neurons(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))
draw_button.pack(pady=20)


window.bind("<Configure>", lambda event: update_canvas(canvas, int(nr_input_neurons.get()), int(nr_hidden_neurons.get()), int(nr_output_neurons.get())))

window.mainloop()
