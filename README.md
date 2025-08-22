# ML Data Sorter

A simple **machine learning + GUI** tool for predicting **1 Field** based on a Excel - database file.

Basic steps: Load the excel containing 2 columns (Feature column, Target column) Fill in the input area with Feature - column type information Hit Start and the model will predict what Target - column type information your input will have.

Built with Python, scikit-learn, pandas, and CustomTkinter.

## Update:
Checks for dropdowns and label indicators

Error handling for scikit count < 2 class

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


