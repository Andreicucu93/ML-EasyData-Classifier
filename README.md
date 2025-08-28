# ML Data Sorter

A simple **machine learning + GUI** tool for predicting **1 Field** based on a Excel - database file.

Basic steps: Load the excel containing 2 columns (Feature column, Target column) Fill in the input area with Feature - column type information Hit Start and the model will predict what Target - column type information your input will have.

## Update:
- Made a single threaded func to wrap load and model_action #8/28/2025
- Check for dropdown #8/22/2025
- Labels for textbox, dropdowns
- Error handling for scikit count < 2 class #8/21/2025

## Features

- Load an Excel dataset with 2 columns

- Currently trains model by 1 attribute

- Predict new entries

- Minimal GUI with CustomTkinter

- Modularized code (separate utils, model, and main GUI app)

## Getting Started

### Prerequisites

- Python 3.9+ (tested on 3.11 / 3.13)

- Install dependencies:


pip install -r requirements.txt


