from result_dictionary_maker import *
from functions import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import pandas as pd

# Cuterle - Palette - RGB
#
# white
# (249, 245, 247)
# #f9f5f7
#
# white-lightblue
# (219, 226, 239)
# #dbe2ef
#
# lightblue
# (63, 113, 175)
# #3f71af
#
# blu
# (17, 48, 78)
# #11304e


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
    l_fasta.configure(text=filename_mod)

    global FASTA_FILE
    FASTA_FILE = filename_mod

    if FASTA_FILE != "" and TSV_FILE != "":
        b_extract_domain.config(state=NORMAL)


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
    l_tsv.configure(text=filename_mod)

    global TSV_FILE
    TSV_FILE = filename_mod

    if FASTA_FILE != "" and TSV_FILE != "":
        b_extract_domain.config(state=NORMAL)


def extract_domains():
    global FASTA_FILE
    global TSV_FILE
    global RESULT_DICTIONARY
    global TABLE_LIST

    t_table.delete(*t_table.get_children())


    check_column_name(TSV_FILE)
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

    # t_table.insert(END, text_to_print)

    if len(TABLE_LIST) > 0:
        b_save_extracted_domains.config(state=NORMAL)

    domains = []
    for everyrow in TABLE_LIST:
        domains.append((f"{everyrow[0]}", f"{everyrow[1]}", f"{everyrow[2]}"))

    for everydomain in domains:
        t_table.insert("", END, values=everydomain)


def save_extracted_domains():
    global RESULT_DICTIONARY
    result_dictionary = RESULT_DICTIONARY

    protein_list = protein_list_maker(FASTA_FILE)

    i = i_counter()

    for everyprotein in protein_list:
        for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:
            protein_accession = everyprotein
            domain_name = everydomain["DOMAIN_NAME"]
            # domain_order = everydomain["DOMAIN_ORDER"]
            start_location = everydomain["START"]
            stop_location = everydomain["STOP"]
            domain_length = everydomain["LENGTH"]
            ip_accession = everydomain["IP_ACCESSION"]
            protein_sequence = result_dictionary[everyprotein]["Sequence"]
            domain_sequence = protein_sequence[start_location:stop_location]

            name_format_dict = {
                    "1": protein_accession,
                    "2": domain_name,
                    "3": domain_length,
                    "4": ip_accession,
                    "5": start_location,
                    "6": stop_location,
                }

            name_format = "1,2,3,4,5,6"

            name_format_choosen = name_format.split(",")
            name_format_string = ">"

            for n in name_format_choosen:
                if n == "1":
                    name_format_string += f" [{name_format_dict[n]}] -"
                elif n == "2":
                    name_format_string += f" [DOMAIN-NAME: {name_format_dict[n]}] -"
                elif n == "3":
                    name_format_string += f" [DOMAIN-LENGTH: {name_format_dict[n]}] -"
                elif n == "4":
                    name_format_string += f" [IP-ACCESSION: {name_format_dict[n]}] -"
                elif n == "5":
                    name_format_string += f" [START: {name_format_dict[n]}] -"
                elif n == "6":
                    name_format_string += f" [STOP: {name_format_dict[n]}] -"

            sliced_text = slice(len(name_format_string) - 2)
            name_format_string_final = name_format_string[sliced_text]

            # If the output file already exists, append the sequences
            try:
                with open("extracted_domains%s.fasta" % i, "a") as file_output:
                    file_output.write(f"{name_format_string_final}\n")
                    file_output.write(f"{domain_sequence}\n\n")

            # ----> IF OUTPUTFILE DOES NOT EXIST, THEN WE CREATE IT WITH THE FIRST SEQUENCE
            except FileNotFoundError:
                with open("extracted_domains%s.fasta" % i, "w") as file_output:
                    file_output.write(f"{name_format_string_final}\n")
                    file_output.write(f"{domain_sequence}\n\n")

    messagebox.showinfo(title="InfoBox", message=f"Extracted sequences saved as\nextracted_domains{i}.fasta")


def reset_all():
    global FASTA_FILE
    global TSV_FILE
    global RESULT_DICTIONARY
    global TABLE_LIST

    FASTA_FILE = ""
    l_fasta.config(text="Select a fasta file")
    TSV_FILE = ""
    l_tsv.config(text="Select a tsv file")
    TABLE_LIST = []
    RESULT_DICTIONARY = {}

    t_table.delete(*t_table.get_children())


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
center_framecomp = Frame(main_window, bg="white", width=1000, height=650, pady=0)

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

center_right_frame = Frame(center_framecomp, bg='white', width=100, height=190)
center_left_frame = Frame(center_framecomp, bg='white', width=400, height=190, padx=3, pady=3)

center_right_frame.grid(row=0, column=1, sticky="")
center_left_frame.grid(row=0, column=0, sticky="")


# Label - fasta
l_fasta = Label(center_left_frame)
l_fasta.config(text="Select a fasta file", bg="white")
l_fasta.grid(column=0, row=0, pady=5)

# Button - search fasta
b_fasta = Button(center_left_frame,
                 text="Browse",
                 command=browse_fasta_file)
b_fasta.grid(column=0, row=1, pady=5)


# Label - tsv
l_tsv = Label(center_left_frame)
l_tsv.config(text="Select a tsv file", bg="white")
l_tsv.grid(column=0, row=2, pady=5)

# Button - search tsv
b_tsv = Button(center_left_frame,
               text="Browse",
               command=browse_tsv_file)
b_tsv.grid(column=0, row=3, pady=5)

# Button - Extract the domain
b_extract_domain = Button(center_left_frame,
                          text="Extract the domains",
                          command=extract_domains,
                          state=DISABLED)
b_extract_domain.grid(column=0, row=4, pady=5)

# Button - Save the extracted domain
b_save_extracted_domains = Button(center_left_frame,
                                  text="Save extracted domains",
                                  command=save_extracted_domains,
                                  state=DISABLED)
b_save_extracted_domains.grid(column=0, row=5, pady=5)

# Button - Reset
b_reset = Button(center_left_frame, text="Reset", command=reset_all)
b_reset.grid(column=0, row=6, pady=50)

# Layout all the widgets in the right frame

# # Label - Table
# t_table = Text(center_right_frame, height=28, width=70)
# t_table.grid(column=0, row=0, sticky="")
#
# scball = Scrollbar(center_right_frame, orient="vertical", command=t_table.yview)
# scball.grid(column=1, row=0, sticky="ns")
#
# t_table["yscrollcommand"] = scball.set


# Tree - table
columns = ("IP_accession", "Domain_name", "Domain_counter")

t_table = ttk.Treeview(center_right_frame, height=28, columns=columns, show="headings")
t_table.heading("IP_accession", text="IP Accession")
t_table.column("IP_accession", width=140, stretch=NO)
t_table.heading("Domain_name", text="Domain name")
t_table.column("Domain_name", width=400, stretch=NO)
t_table.heading("Domain_counter", text="Domain counter")
t_table.column("Domain_counter", width=160, stretch=NO)
t_table.grid(column=0, row=0, sticky="nsew")

scrollbar = ttk.Scrollbar(center_right_frame, orient=VERTICAL, command=t_table.yview)
t_table["yscrollcommand"] = scrollbar.set
scrollbar.grid(column=1, row=0, sticky="ns")


main_window.mainloop()
