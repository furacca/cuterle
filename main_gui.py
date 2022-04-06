from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


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


# ****************************************************
# Global variable
# ****************************************************
FONT_NAME = "Courier"

# ****************************************************
# Create the window
main_window = Tk()
main_window.title("Cuterle")
main_window.geometry("{}x{}".format(1000, 800))

# ****************************************************
# Create all the main containers
# ****************************************************
top_frame = Frame(main_window, bg="white", width=1000, height=150)
left_frame = Frame(main_window, bg="blue", width=250, height=650, pady=3)
right_frame = Frame(main_window, bg="green", width=750, height=650, pady=3)

# ****************************************************
# Layout all the main containers
# ****************************************************
main_window.grid_rowconfigure(1, weight=1)
main_window.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, columnspan=2, stick="nsew")
left_frame.grid(row=1, column=0, stick="nsew")
# left_frame.grid_propagate(0)
right_frame.grid(row=1, column=1, stick="nsew")
# right_frame.grid_propagate(0)

# ****************************************************
# Layout all the widgets in the top frame
# ****************************************************
logo = Image.open("./screenshots/00_logo.png")
resized_logo = logo.resize((650, 200), Image.LANCZOS)
new_logo = ImageTk.PhotoImage(resized_logo)
logo_label = Label(top_frame, image=new_logo, background="white")
logo_label.grid()

# ****************************************************
# Layout all the widgets in the left frame
# ****************************************************

# Label - fasta
l_fasta = Label(left_frame)
l_fasta.config(text="Select a fasta file")
l_fasta.grid(column=0, row=0)


# Button - search fasta
b_fasta = Button(left_frame, text="Browse", command=browse_fasta_file)
b_fasta.grid(column=0, row=1)


# Layout all the widgets in the right frame







#
# # Label - Logo
# l_logo = tkinter.Label(frame1)
# l_logo.config(text="Questo è il logo",
#               font=(FONT_NAME, 5, "bold"),
#               width=30)
# l_logo.grid(column=0, row=0)
#
# # Label - tsv
# l_tsv = tkinter.Label(frame2)
# l_tsv.config(text="TSV")
# l_tsv.grid(column=1, row=1)
#
# # Button - search tsv
# b_tsv = tkinter.Button(frame2, text="Browse", command=browse_fasta_file)
# b_tsv.grid(column=1, row=2)
#

#

main_window.mainloop()
