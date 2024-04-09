import os
import tkinter as tk
import ttkbootstrap as ttk


from tkinter import filedialog
from tkinter import Radiobutton
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import Listbox


from SubtitleService import SubtitleService
from page import Page
import Constants
from ToolTip import CreateToolTip


# Start page from the program
class StartPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        # For simplifying the row placement of the widgets
        # managed with the self.row_handle function, just insert the function instead of the row integer
        self.row_count = 0

        self.list_font = ("Helvetica", 22)
        self.text_font = ("Helvetica", 20)
        self.label_font = ("Arial", 25)

        s = ttk.Style()
        s.configure("my.TButton", font=self.text_font)

        s = ttk.Style()
        s.configure("TCheckbutton", font=self.list_font)

        self.subtitle_service = SubtitleService()
        self.file_path = None

        # Top description of what to do in the segment of the GUI
        # First Step
        # Selecting the video file

        # Label for the file explorer
        self.file_explorer_label = self.label("1. Select the video for transcription")
        self.insert(
            self.file_explorer_label, ipadx=5, ipady=5, padx=15, pady=5, stick="nsew"
        )
        self.insert(
            self.file_explorer_label, ipadx=5, ipady=5, padx=15, pady=5, stick="nsew"
        )

        # Bulk/Batch-mode checkbox
        self.bulk_var = BooleanVar()
        self.bulk_checkbox = ttk.Checkbutton(
            self,
            text="Batch-/Bulk-Mode",
            variable=self.bulk_var,
            onvalue=True,
            offvalue=False,
        )
        bulk_button_row = self.row_handle()
        self.insert(self.bulk_checkbox, row=bulk_button_row, padx=80, pady=20)
        bulk_tool_tip_button = ttk.Button(self, text="?", state='disabled')
        self.insert(bulk_tool_tip_button, row=bulk_button_row, padx=80, pady=20, stick="e")
        bulk_tool_tip = CreateToolTip(
            bulk_tool_tip_button,
            "Transcribes/translates all files inside the folder with the same extension (for example .mp4) as the selected file.",
        )

        # Button for opening the file explorer and choosing a file
        file_explorer_button = self.create_button("Select a file", self.browseFiles)

        # Label for showing the name of the chosen file
        self.label_chosen_file = self.text("")
        self.insert(self.label_chosen_file, columnspan=2, ipadx=0, ipady=0, padx=12)

        # Separator for the first segment
        self.create_separator()

        # Second Step
        # Selecting the output types

        # Label for the extension option
        self.type_select_label = self.create_label("2. Select your output files")

        # Choose option for the desired output file either .txt or .srt

        # Bool variables for giving the checkboxes for the format select a value
        self.format_checkbox_variables = []
        for item in Constants.subtitle_types:
            self.format_checkbox_variables.append(BooleanVar())

        self.create_checkboxes(self.format_checkbox_variables, Constants.subtitle_types)

        # Separator for the second segment
        self.create_separator()

        # Third step
        # Select if the subtitles should be in english as well

        # Label for the selection for the language of the subtitles
        language_select_label = self.create_label(
            "3. Select the languages for subtitles"
        )

        # Choose option for the desired language
        self.language_checkbox_variables = []
        for item in Constants.languages:
            self.language_checkbox_variables.append(BooleanVar())

        self.create_checkboxes(self.language_checkbox_variables, Constants.languages)

        # Separator for the third segment
        self.create_separator()

        # Fourth step
        # Start the process

        # Label for the start of the transcription
        startButtonLabel = self.create_label("4. Start the transcription")

        # Button for starting the process
        startButton = self.create_button("Start", self.start_transcription)

        # Progression Label
        self.progress_label = self.create_label("")

        # Saved to text
        self.saved_to_text = self.text("")
        self.insert(self.saved_to_text)

        # Error Label
        self.error_label = ttk.Label(
            self, text="", foreground="red", font=self.text_font
        )
        self.insert(self.error_label, padx=12, pady=15, stick="n")

    # increments the row to make sure you can just add a widget at the place in the code where it should be on the page without minding the rows
    def row_handle(self):
        self.row_count += 1
        return self.row_count

    # Returns a label
    def label(self, label_text: str) -> ttk.Label:
        return ttk.Label(
            self, text=label_text, bootstyle="primary", font=self.label_font
        )

    # Returns text, by setting the font to the text font
    def text(self, text: str) -> ttk.Label:
        return ttk.Label(self, text=text, font=self.text_font)

    # Returns a Button
    def button(self, text: str, command) -> ttk.Button:
        return ttk.Button(self, text=text, command=command, style="my.TButton")

    # Creates, inserts and returns a label
    def create_label(self, label_text: str) -> ttk.Label:
        label = self.label(label_text)
        self.insert(label, ipadx=5, ipady=10, padx=15, pady=15, stick="nsew")
        return label

    # Creates, inserts and returns a button
    def create_button(self, text: str, command) -> ttk.Button:
        button = self.button(text, command)
        self.insert(button, padx=80)
        return button

    # Creates a separator
    def create_separator(self, row=None) -> None:
        separator = ttk.Separator(self, orient="horizontal")
        self.insert(separator, row, ipadx=0, ipady=0, padx=0, pady=0)

    # Creates a checkbox array with given List
    def create_checkboxes(self, checkbox_variables, display_strings):
        # initial padx and the var for making sure there can be more checkboxes next to each other
        padx_var = 40
        row_for_check_buttons: int
        # creating checkboxes for every format type in Constants.py with the declared boolean value
        for index, item in enumerate(checkbox_variables):
            checkbox = ttk.Checkbutton(
                self,
                text=display_strings[index],
                variable=item,
                onvalue=True,
                offvalue=False,
            )
            # To ensure there are only 4 select options per row
            if (index % 3) == 0:
                row_for_check_buttons = self.row_handle()
                padx_var = 40
            self.insert(checkbox, row=row_for_check_buttons, padx=padx_var, pady=15)
            padx_var += 120

    # Inserts the given ttk object to the page
    def insert(
        self,
        object: ttk.ttk,
        row=None,
        column=0,
        columnspan=1,
        ipadx=0,
        ipady=0,
        padx=0,
        pady=0,
        stick="nsew",
    ) -> None:
        # if no row is explicitly given it gets the next row from the handler and calls the function again with the row number
        if row == None:
            row = self.row_handle()
            self.insert(
                object, row, column, columnspan, ipadx, ipady, padx, pady, stick
            )
        else:
            object.grid(
                row=row,
                column=column,
                columnspan=columnspan,
                ipadx=ipadx,
                ipady=ipady,
                padx=padx,
                pady=pady,
                stick=stick,
            )

    # Starts the transcription process
    def start_transcription(self) -> None:
            # Starts the transcription process based on the selected file, file types, and languages.
            # If any required selection is missing, it displays an error message.
            format_checkbox_selected = self.check_if_checkbox_is_selected(
                self.format_checkbox_variables
            )
            language_checkbox_selected = self.check_if_checkbox_is_selected(
                self.language_checkbox_variables
            )
            if (
                self.file_path is None
                and not format_checkbox_selected
                and not language_checkbox_selected
            ):
                self.error_label.configure(text="Select a file, a filetype and a language")
                return
            elif not format_checkbox_selected and not language_checkbox_selected:
                self.error_label.configure(text="Select a filetype and a language")
            elif self.file_path is None and not format_checkbox_selected:
                self.error_label.configure(text="Select a file and a filetype")
            elif self.file_path is None and not language_checkbox_selected:
                self.error_label.configure(text="Select a file and a language")
            elif self.file_path is None:
                self.error_label.configure(text="Select a file")
                return
            elif not format_checkbox_selected:
                self.error_label.configure(text="Select a filetype")
                return
            elif not language_checkbox_selected:
                self.error_label.configure(text="Select a language")

            else:
                self.error_label.configure(text="")
                self.progress_label.configure(text="In progress", foreground="red")
                self.update()  # needed to display the In progress otherwise the frame for displaying it wouldn't be rendered
                filetypes = self.checkbox_variables_to_string_list_file_types()
                languages = self.checkbox_variables_to_string_list_languages()
                self.subtitle_service.create_subtitles(
                    self.file_path, languages, filetypes, self.bulk_var.get()
                )
                self.progress_label.configure(text="DONE", foreground="green")
                saved_to = (
                    "Saved to: "
                    + os.path.split(self.file_path)[0][
                        len(os.path.split(self.file_path)[0]) - 30 :
                    ]
                )
                self.saved_to_text.configure(text=saved_to, foreground="green")

    # Selecting a file and saving its path
    def browseFiles(self) -> None:
        # file picker
        self.file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select a File",
            filetypes=(("Video Files", "*.mp4"), ("Sound File", "*.mp3")),
        )

        # Showing the last 25 chars from the path to the user
        self.label_chosen_file.configure(
            text="File Opened:\n..." + self.file_path[len(self.file_path) - 25 :]
        )

    # converts the checkbox variables from the format/filetypes and converts the booleans into
    # the coherent string variables
    def checkbox_variables_to_string_list_file_types(self) -> list[str]:
        format_list = []
        for index, item in enumerate(self.format_checkbox_variables):
            if item.get():
                format_list.append(Constants.subtitle_types[index])
        return format_list

    def checkbox_variables_to_string_list_languages(self) -> list[str]:
        language_list = []
        for index, item in enumerate(self.language_checkbox_variables):
            if item.get():
                language_list.append(Constants.language_abbreviations[index])
        return language_list

    def check_if_checkbox_is_selected(self, checkboxes: list[BooleanVar]) -> bool:
        for item in checkboxes:
            if item.get():
                return True
        return False
