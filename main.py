from tkinter import filedialog
import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel
import os
import numpy as np
import utils
import model as ml

root = CTk()
root.title("New entry predictor")
root.geometry("600x400")

selected_path = {'file': None}


def choose_and_load():
    file_path = filedialog.askopenfilename(
        title='Select an excel type database file',
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if file_path:
        df = utils.load_excel(file_path)
        print(df.head())
        selected_path['file'] = file_path
        return df
    else:
        print('No file selected')
        return None
    
def start_model_action():
    if not selected_path['file']:
        print('No file selected.')
        return
    ml.run_model(selected_path['file'])


def start_widgets():
    main_frame = CTkFrame(root)
    main_frame.grid(row=1, column=1, pady=10, padx=10)

    load_button = CTkButton(main_frame, text='Load database', command=choose_and_load)
    load_button.grid(row=1, column=1, pady=10, padx=10)

    start_model = CTkButton(main_frame, text='Start', command=start_model_action)
    start_model.grid(row=2, column=1, pady=10, padx=10)

start_widgets()

    
root.mainloop()