import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

full_data = pd.DataFrame()
remaining_data = pd.DataFrame()
is_data_normalized = False 

def open_file():
    global full_data, remaining_data
    file_path = filedialog.askopenfilename(title="Selectează un fișier", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        print(f"Fișier deschis: {file_path}") 
        full_data = pd.read_csv(file_path)

        selected_columns = ["Year", "Publisher", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales", "Rank"]
        full_data = full_data[selected_columns]
        
        sample_data = full_data.sample(frac=0.5)
        remaining_data = full_data.drop(sample_data.index)

        for item in tree.get_children():
            tree.delete(item)

        for index, row in sample_data.iterrows():
            tree.insert("", "end", values=row.tolist())
        
        print(f"Numărul de rânduri inițial: {full_data.shape[0]}")
        print(f"Numărul de rânduri rămase: {remaining_data.shape[0]}")

def normalize_data():
    global full_data, is_data_normalized

    full_data[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]] = \
        full_data[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    is_data_normalized = True
    print("Date normalizate.")

    for item in tree_normalized.get_children():
        tree_normalized.delete(item)

    for index, row in full_data.iterrows():
        tree_normalized.insert("", "end", values=row.tolist())

    notebook.tab(tab2, state="normal")

def use_remaining_data():
    global remaining_data
    if not remaining_data.empty:
        print("Folosind restul de date:")
        for index, row in remaining_data.iterrows():
            print(row.tolist())  
        remaining_data = pd.DataFrame()  

def update_button_visibility(event):
    selected_tab = notebook.index(notebook.select())
    
    if is_data_normalized:
        notebook.tab(tab2, state="normal")  
    else:
        notebook.tab(tab2, state="disabled")  

def on_tab_change(event):
    selected_tab = notebook.index(notebook.select())

    if selected_tab == 1 and not is_data_normalized:
        messagebox.showwarning("Atenție", "Trebuie să normalizezi datele înainte de a accesa această filă.")
        notebook.select(0)  


main_window = tk.Tk()
main_window.title("Games Rank")
main_window.geometry("1920x950")
main_window.configure(bg="#2E3B4E")


notebook = ttk.Notebook(main_window, style="TNotebook")
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab1 = ttk.Frame(notebook, padding=10)
tab2 = ttk.Frame(notebook, padding=10)
tab3 = ttk.Frame(notebook, padding=10)
tab4 = ttk.Frame(notebook, padding=10)

notebook.add(tab1, text="Date de intrare")
notebook.add(tab2, text="Date de intrare normalizate")
notebook.add(tab3, text="Antrenare")
notebook.add(tab4, text="Testare")


columns = ["Year", "Publisher", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales", "Rank"]
tree = ttk.Treeview(tab1, columns=columns, show="headings", height=15)


style = ttk.Style()
style.configure("Treeview",
                background="#ffffff",
                foreground="black",
                rowheight=30,
                fieldbackground="#f0f0f0")
style.map("Treeview", background=[("selected", "#3DA4D6")])

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor='center')

scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
scrollbar.grid(row=0, column=1, sticky="ns")

tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(0, weight=1)


tree_normalized = ttk.Treeview(tab2, columns=columns, show="headings", height=15)

for col in columns:
    tree_normalized.heading(col, text=col)
    tree_normalized.column(col, width=120, anchor='center')

scrollbar_normalized = ttk.Scrollbar(tab2, orient="vertical", command=tree_normalized.yview)
tree_normalized.configure(yscroll=scrollbar_normalized.set)

tree_normalized.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
scrollbar_normalized.grid(row=0, column=1, sticky="ns")

tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(0, weight=1)


button_frame = ttk.Frame(main_window)
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

button_style = ttk.Style()
button_style.configure("Custom.TButton",
                       background="#4CAF50",
                       foreground="black",
                       font=("Arial", 12, "bold"),
                       padding=(10, 5))
button_style.map("Custom.TButton", background=[("active", "#45a049")])

open_button = ttk.Button(button_frame, text="Deschide", command=open_file, style="Custom.TButton")
save_button = ttk.Button(button_frame, text="Salveaza", style="Custom.TButton")
normalize_button = ttk.Button(button_frame, text="Normalizare", command=normalize_data, style="Custom.TButton")

open_button.grid(row=0, column=0, padx=5, pady=5)
save_button.grid(row=0, column=1, padx=5, pady=5)
normalize_button.grid(row=0, column=2, padx=5, pady=5)


notebook.tab(tab2, state="disabled")

update_button_visibility(None)


notebook.bind("<<NotebookTabChanged>>", update_button_visibility)
notebook.bind("<<NotebookTabChanged>>", on_tab_change)  


main_window.mainloop()
