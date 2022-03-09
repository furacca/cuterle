import os
import fnmatch
import pandas as pd
from Bio import SeqIO
from logo import logo
from functions import print_file_in_the_folder
from functions import check_column_name
from functions import existence_file_check


# START
print(logo)
print("Welcome, this is CUTERLE.")

# GIVE THE TSV FILE AS INPUT
print("\nThe output of an InterPro scan is a <file.tsv>. I need it to obtain the domains' coordinates.")
print("In the current folder you have the following *.tsv files:")
print_file_in_the_folder("*.tsv")

# WHILE LOOP TO CHECK THE EXISTENCES OF THE INPUT FILE .tsv
while True:
    tsv_file = input("Type the file name using this format -> file.tsv : ")
    if existence_file_check(tsv_file, "*.tsv") == True:
        break
    else:
        print(f"{tsv_file} doesn't exist or doesn't has .tsv extension. Retry.")
        pass

# GIVE THE FASTA FILE AS INPUT
print("\nNow type the name of the <file.fasta>. ")
print("It's imperative that the protein accession in the file.fasta is the same of the sequences submitted to InterPro.")
print("In the current folder you have the following *.fasta files:")
print_file_in_the_folder("*.fasta")

# WHILE LOOP TO CHECK THE EXISTENCES OF THE INPUT FILE .fasta
while True:
    fasta_file = input("Type the file name using this format -> file.fasta : ")
    if existence_file_check(fasta_file, "*.fasta") == True:
        break
    else:
        print(f"{fasta_file} doesn't exist or doesn't has .fasta extension. Retry.")
        pass

# CHECK (AND EVENTUALLY ADD) IF THE FILE ALREADY HAS COLUMNS' NAME (0, 2, 3, ... )
check_column_name(tsv_file)

# CREATE WITH PANDAS A NEW DATAFRAME
dataframe_file_tsv = pd.read_table(tsv_file)

# COUNT HOW MANY RESULTS THERE ARE
result_of_analysis = dataframe_file_tsv.loc[dataframe_file_tsv["3"] == "Pfam"]
number_of_result_of_analysis = int(len(result_of_analysis))

# CREATE A DICTIONARY WITH THE RESULT OF
results_dictionary = result_of_analysis.to_dict("records")

# COUNTER TO RENAME OUTPUT FILE WHEN ANOTHER FILE WITH THE SAME NAME EXISTS
list_of_file = os.listdir("./")
if "extracted_domains.fasta" in list_of_file:
    i = 1
    while os.path.exists("extracted_domains%s.fasta" % i):
        i += 1
else:
    i = ""

# er = Every Result
for er in range(0, number_of_result_of_analysis):
    prot_accession = results_dictionary[er]["0"]
    seq_lenght = results_dictionary[er]["2"]
    signature_description = results_dictionary[er]["5"]
    start_location = results_dictionary[er]["6"]
    stop_location = results_dictionary[er]["7"]
    interpro_annotation = results_dictionary[er]["12"]

    with open(fasta_file) as elenco_fasta:
        for record in SeqIO.parse(elenco_fasta, "fasta"):
            if record.id == prot_accession:
                sequenza = f"{record.seq}"

    seq_dominio = sequenza[start_location:stop_location]

    try:
        with open("extracted_domains%s.fasta" % i, "a") as file_output:
            file_output.write("\n")
            file_output.write(f">{prot_accession} - {signature_description} - {interpro_annotation}")
            file_output.write("\n")
            file_output.write(seq_dominio)
    except FileNotFoundError:
        with open("extracted_domains%s.fasta" % i, "w") as file_output:
            file_output.write(f">{prot_accession} - {signature_description} - {interpro_annotation}\n")
            file_output.write(seq_dominio)


print(f"\n\nTAAAAC! Done. {number_of_result_of_analysis} domain has been extracted for you.")
print(f"You can find your results in extracted_domains%s.fasta" %i)