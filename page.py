import tkinter as tk
from tkinter import ttk


# The blueprint for a page/frame
class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
