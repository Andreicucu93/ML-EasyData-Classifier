from tkinter import filedialog
import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkTextbox, CTkOptionMenu
import os
import numpy as np
import utils
import model as ml

root = CTk()
root.title("ML Data Sorter - predicts new data information")
root.geometry("700x600") #w h

selected_path = {'file': None}

def fuct():
    pass

def choose_and_load():   ## SELECT feature_column & target_column FROM LOADED df COLUMNS
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
    
def get_input():
    raw = textbox.get("1.0", "end-1c")
    items = [s.strip() for s in raw.splitlines() if s.strip()]
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
        print('Please select the dropdown attributes.')

        return
    ml.run_model_1target(selected_path['file'], 
    feature_column=feat, 
    target_column_1=targ,
    new_products=get_input())


def start_widgets():   ## POPULATE dropdown for Feature and Target attributes
    global textbox, feature_attr_dropdown, target_attr_dropdown
    buttons_frame = CTkFrame(root)  #For buttons
    buttons_frame.grid(row=1, column=1, pady=10, padx=10)

    textbox_frame = CTkFrame(root) #For textbox
    textbox_frame.grid(row=1, column=0, pady=10, padx=10)

    options_frame = CTkFrame(root)
    options_frame.grid(row=2, column=0, pady=10, padx=10)

    load_button = CTkButton(buttons_frame, text='Load dataset', command=choose_and_load)
    load_button.grid(row=1, column=1, pady=10, padx=10)

    start_model = CTkButton(buttons_frame, text='Start', command=start_model_action)
    start_model.grid(row=2, column=1, pady=10, padx=10)

    test_button = CTkButton(buttons_frame, text='test', command=get_input)
    test_button.grid(row=3, column=1, pady=10, padx=10)

    textbox = ctk.CTkTextbox(textbox_frame, width=350, height=450)
    textbox.grid(row=0, column=0, pady=10, padx=10)

    feature_attr_dropdown = CTkOptionMenu(options_frame, values=[' -- load a file first --'], width=200)
    feature_attr_dropdown.grid(row=0, column=0, padx=15, pady=10)

    target_attr_dropdown = CTkOptionMenu(options_frame, values=[' -- load a file first --'], width=200)
    target_attr_dropdown.grid(row=0, column=1, padx=15, pady=10)

start_widgets()

    
root.mainloop()