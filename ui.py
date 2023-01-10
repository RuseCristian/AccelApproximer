from tkinter import *
from tkinter import ttk

import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('400x200')


# Text Widget
rpm_torque_textBox = tk.Text(window, width=20, height=3)
rpm_torque_textBox.grid(column=1, row=15)

gear_ratio_textBox = tk.Text(window, width=20, height=1)
gear_ratio_textBox.grid(column=1, row=40)
gear_ratio_textBox.config(wrap='none')

window.mainloop()
