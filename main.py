from tkinter import filedialog, ttk
import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkTextbox, CTkOptionMenu
from CTkMessagebox import CTkMessagebox
import os
import numpy as np
import utils
import model as ml
import threading

## 8/22/25
#Check for dropdown
#Labels for textbox, dropdowns
#Error handling for scikit count < 2 class

root = CTk()
root.title("ML EasyData Classifier")
root.geometry("1250x600") #w h
selected_path = {'file': None}


def clear_treeview():
    for item in tree.get_children():
        tree.delete(item)    
    print('Cleared treeview.')

def get_input():
    raw = textbox.get("1.0", "end-1c")
    items = [s.strip() for s in raw.splitlines() if s.strip()]
    if not items:
        CTkMessagebox(title='Warning', message='Please input at least one item.', icon='warning')
        print("missing textbox input")
        return None
    col1 = feature_attr_dropdown.get()
    print(col1)
    return items


def start_model_action():
    if not selected_path['file']:
        print('No file selected.')
        return
    
    feat = feature_attr_dropdown.get()
    targ = target_attr_dropdown.get()
    if feat.startswith('--') or targ.startswith('--'):
        on_dropdown_change()
        return
    items = get_input()
    if not items:
        return
    
    try:
        predict_output = utils.export_data(dataset=ml.run_model_1target(selected_path['file'], 
        feature_column=feat, 
        target_column_1=targ,
        new_products=get_input()))

        for _, row in predict_output.iterrows():
            tree.insert('', 'end', values=row.tolist())
    except Exception as e:
        msg = class_error(e)
        CTkMessagebox(title='Error', message=msg, icon='cancel')


def run_asynk(func, btn:CTkButton, start_text:str, done_text:str):
    def worker():
        root.after(0, lambda: btn.configure(text=start_text, state='disabled'))
        func()
        root.after(0, lambda: btn.configure(text=done_text, state='normal'))
    threading.Thread(target=worker, daemon=True).start()


def choose_and_load():
    file_path = filedialog.askopenfilename(
        title='Select an excel type database file',
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if file_path:
        df = utils.load_excel(file_path)
        print(df.head())
        selected_path['file'] = file_path
        loaded_columns = df.columns
        print(loaded_columns)

        feature_attr_dropdown.configure(values=list(df.columns), dropdown_fg_color='lime green', fg_color='forest green')
        feature_attr_dropdown.set('-- Select Feature column --')

        target_attr_dropdown.configure(values=list(df.columns), dropdown_fg_color='lime green', fg_color='forest green')
        target_attr_dropdown.set('-- Select Target column --')

        return df
    else:
        print('No file selected')
        return None


def start_model_action():
    if not selected_path['file']:
        print('No file selected.')
        return
    
    feat = feature_attr_dropdown.get()
    targ = target_attr_dropdown.get()
    if feat.startswith('--') or targ.startswith('--'):
        on_dropdown_change()
        return
    items = get_input()
    if not items:
        return
    
    try:
        predict_output = utils.export_data(dataset=ml.run_model_1target(selected_path['file'], 
        feature_column=feat, 
        target_column_1=targ,
        new_products=get_input()))

        for _, row in predict_output.iterrows():
            tree.insert('', 'end', values=row.tolist())
    except Exception as e:
        msg = class_error(e)
        CTkMessagebox(title='Error', message=msg, icon='cancel')


#Warnings
def _is_selected(val:str) -> bool:          #Checks if the dropdown holds a real selection and not placeholder
    return bool(val) and not val.startswith('--')

def on_dropdown_change(_value=None):        #Checks and reminds the user to make selections from dropdowns
    if _is_selected(feature_attr_dropdown.get()) and _is_selected(target_attr_dropdown.get()):
        dropdown_label.configure(text='')
    else:
        dropdown_label.configure(text='Please make the dropdown selections.', text_color='red')

def class_error(err: Exception) -> str:
    s = str(err)
    if "least populated class" in s:
        return ("Your selected target column has a class with only ONE row.\n"
        "To train, each class needs at least 2 examples.\n"
        "Fix: add more rows for that class, or remove it from the dataset")
    return s


def start_widgets():   ## POPULATE dropdown for Feature and Target attributes
    global textbox, feature_attr_dropdown, target_attr_dropdown, tree, dropdown_label, load_button, start_button
    buttons_frame = CTkFrame(root)          #For buttons - control
    buttons_frame.grid(row=1, column=2, pady=10, padx=10)

    textbox_frame = CTkFrame(root)          #For textbox - input
    textbox_frame.grid(row=1, column=0, padx=10)

    treeview_frame = CTkFrame(root)         #For treeview - output
    treeview_frame.grid(row=1, column=1, pady=(55, 10), padx=10)

    options_frame = CTkFrame(root)          #For dropdowns - attributes
    options_frame.grid(row=2, column=0, padx=10)

    load_button = CTkButton(buttons_frame, text='Load dataset', command=lambda: run_asynk(func=choose_and_load, btn=load_button, start_text='Loading ⌛..', done_text='Load dataset'))
    load_button.grid(row=1, column=1, pady=10, padx=10)

    start_button = CTkButton(buttons_frame, text='Start', command=lambda: run_asynk(func=start_model_action, btn=start_button, start_text='Analysing ⌛..', done_text='Start'))
    start_button.grid(row=2, column=1, pady=10, padx=10)

    clear_button = CTkButton(buttons_frame, text='Clear output', command=clear_treeview, fg_color='firebrick3')
    clear_button.grid(row=3, column=1, pady=(10, 0))

    textbox_label = CTkLabel(textbox_frame, text='Enter items (one per line):')
    textbox_label.grid(row=0, column=0)

    textbox = CTkTextbox(textbox_frame, width=350, height=380)
    textbox.grid(row=1, column=0, pady=10, padx=10)

    dropdown_label = CTkLabel(options_frame, text= '')
    dropdown_label.grid(row=1, column=0, columnspan=2)

    feature_attr_dropdown = CTkOptionMenu(options_frame, values=[' -- load a file first --'], width=200, command=on_dropdown_change)
    feature_attr_dropdown.grid(row=0, column=0, padx=15)

    target_attr_dropdown = CTkOptionMenu(options_frame, values=[' -- load a file first --'], width=200, command=on_dropdown_change)
    target_attr_dropdown.grid(row=0, column=1, padx=15)


    tree = ttk.Treeview(treeview_frame, height=20)
    tree['columns'] = ('Data', 'Prediction')
    tree.column('#0', width=0, stretch=False)
    tree.column('Data', anchor='w', width=200)
    tree.column('Prediction', anchor='center', width=300)
    #Reminder: heading controls title/anchor
    tree.heading('#0', text='', anchor='w')
    tree.heading('Data', text='Data in', anchor='center')
    tree.heading('Prediction', text='Prediction out', anchor='center')
    tree.grid(row=0, column=0)

start_widgets()

    
root.mainloop()