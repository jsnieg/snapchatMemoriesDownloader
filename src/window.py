# App with UI from Tkinter

import tkinter as tk
from tkinter import filedialog


# create only once not upon func invoke everytime
root = tk.Tk()


def show_window():
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path