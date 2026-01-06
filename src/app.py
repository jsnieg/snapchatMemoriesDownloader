# App with UI from Tkinter

import tkinter as tk
from tkinter import filedialog


class App():
    ...


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)