import tkinter

from result_dictionary_maker import *
from functions import *
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import pandas as pd


def browse_fasta_file():
    filename = filedialog.askopenfilename(initialdir="./",
                                          title="Select a fasta file",
                                          filetypes=(("Fasta files",
                                                      "*.fasta"),
                                                     ("all files", "*.*")
                                                     ))
    temp_list = filename.split("/")
    tempo_list_length = len(temp_list)
    filename_mod = temp_list[tempo_list_length-1]
    l_fasta.configure(text="File opened: \n" + filename_mod)

    global FASTA_FILE
    FASTA_FILE = filename_mod


def browse_tsv_file():
    filename = filedialog.askopenfilename(initialdir="./",
                                          title="Select a tsv file",
                                          filetypes=(("TSV files",
                                                      "*.tsv"),
                                                     ("all files", "*.*")
                                                     ))
    temp_list = filename.split("/")
    tempo_list_length = len(temp_list)
    filename_mod = temp_list[tempo_list_length-1]
    l_tsv.configure(text="File opened: \n" + filename_mod)

    global TSV_FILE
    TSV_FILE = filename_mod


def extract_domains():
    global FASTA_FILE
    global TSV_FILE
    global RESULT_DICTIONARY
    global TABLE_LIST

    protein_list = protein_list_maker(FASTA_FILE)
    dataframe_tsv = pd.read_table(TSV_FILE)
    prior_choice = ""
    fasta_file = FASTA_FILE
    domain_order = "Increasing"

    RESULT_DICTIONARY = result_dictionary_maker(protein_list, dataframe_tsv, prior_choice, fasta_file, domain_order)

    TABLE_LIST = create_table_row_list(RESULT_DICTIONARY)

    text_to_print = ""
    for everydomain in TABLE_LIST:
        new_line = f"{everydomain[0]}\t\t{everydomain[1]}\t\t\t\t\t{everydomain[2]}\n"
        text_to_print += new_line

    t_table.insert(END, text_to_print)


# ****************************************************
# Global variable
# ****************************************************
FONT_NAME = "Courier"
TSV_FILE = ""
FASTA_FILE = ""
RESULT_DICTIONARY = {}
TABLE_LIST = []
# ****************************************************
# Create the window
main_window = Tk()
main_window.title("Cuterle")
main_window.geometry("{}x{}".format(1000, 800))

# ****************************************************
# Create all the main containers
# ****************************************************
top_frame = Frame(main_window, bg="white", width=1000, height=150)
center_framecomp = Frame(main_window, bg="red", width=1000, height=650, pady=3)

# ****************************************************
# Layout all the main containers
# ****************************************************
main_window.grid_rowconfigure(1, weight=1)
main_window.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, columnspan=2, stick="nsew")
center_framecomp.grid(row=1, column=0, stick="nsew")
# left_frame.grid_propagate(0)


# ****************************************************
# TOP FRAME
# ****************************************************

# Create all the widget of the top frame
logo = Image.open("./screenshots/00_logo.png")
resized_logo = logo.resize((650, 200), Image.LANCZOS)
new_logo = ImageTk.PhotoImage(resized_logo)
logo_label = Label(top_frame, image=new_logo, background="white")

# Layout all the widget of the top frame
logo_label.grid()

# ****************************************************
# CENTER
# ****************************************************

# Create the center widgets
center_framecomp.grid_rowconfigure(0, weight=1)
center_framecomp.grid_columnconfigure(1, weight=1)

center_right_frame = Frame(center_framecomp, bg='blue', width=100, height=190)
center_left_frame = Frame(center_framecomp, bg='yellow', width=400, height=190, padx=3, pady=3)

center_right_frame.grid(row=0, column=1, sticky="nsew")
center_left_frame.grid(row=0, column=0, sticky="ns")


# Label - fasta
l_fasta = Label(center_left_frame)
l_fasta.config(text="Select a fasta file")
l_fasta.grid(column=0, row=0)

# Button - search fasta
b_fasta = Button(center_left_frame, text="Browse", command=browse_fasta_file)
b_fasta.grid(column=0, row=1)

# Label - tsv
l_tsv = Label(center_left_frame)
l_tsv.config(text="Select a fasta file")
l_tsv.grid(column=0, row=2)

# Button - search tsv
b_tsv = Button(center_left_frame, text="Browse", command=browse_tsv_file)
b_tsv.grid(column=0, row=3)

# Button - Extract the domain
b_tsv = Button(center_left_frame, text="Extract the domains", command=extract_domains)
b_tsv.grid(column=0, row=4)





# Layout all the widgets in the right frame
# # Label - Table
# l_table = Label(center_right_frame, height=200, width=300)
# l_table.config(text="")
# l_table.grid(column=0, row=0)

# Text - Table
#

t_table = Text(center_right_frame, height=25, width=75)
t_table.grid(column=0, row=0)

scball = Scrollbar(center_right_frame, orient="vertical", command=t_table.yview)
scball.grid(column=1, row=0, sticky="ns")

t_table["yscrollcommand"] = scball.set




main_window.mainloop()
