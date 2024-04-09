import tkinter as tk
from tkinter import ttk
from page import Page
from StartPage import StartPage


# The Application (the backbone of the GUI)
class App(tk.Tk):
    # __init__ function for the App class
    def __init__(self, *args, **kwargs):
        # __init function for the TK class
        tk.Tk.__init__(self, *args, **kwargs)

        # Metadata for the GUI window
        self.title("Whisper GUI")
        
        # creating a container/frame as the root layer
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # initializing an empty dictionary for the pages/frames
        self.frames = {}

        # iterating through each page class and initializing them
        for F in (Page, StartPage):
            frame = F(container, self)

            # putting the pages in the dictionary
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Starts the Application with the StartPage
        self.showFrame(StartPage)

    # function for raising the frame/showing the new frame
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
