from functions import *
from drawer import *
from tabulate import tabulate
from asciithing import *
from Bio import SeqIO
import pandas as pd
import os

# *********************************************************************************************
# START
# *********************************************************************************************
print(logo)
print(separator)
print("Welcome, this is CUTERLE, \n"
      "a bioinformatic tool which return an output file containing every domain annotated by InterProScan\n"
      "via Pfam or SMART analysis from the list of protein submitted.")

# *********************************************************************************************
# GIVE THE TSV FILE AS INPUT
# *********************************************************************************************
print(separator)
print("The first file requested is the one with ~.tsv extension which contains the domains coordinates.")
print("In the current folder you have the following *.tsv files:")
print_file_in_the_folder("*.tsv")

# *********************************************************************************************
# WHILE LOOP TO CHECK THE EXISTENCES OF THE INPUT FILE .tsv
# *********************************************************************************************
while True:
    tsv_file = input("Type the file name using this format -> file.tsv : ")
    if existence_file_check(tsv_file, "*.tsv") == True:
        break
    else:
        print(f"{tsv_file} doesn't exist or doesn't has .tsv extension. Retry.")
        pass

# *********************************************************************************************
# GIVE THE FASTA FILE AS INPUT
# *********************************************************************************************
print(separator)
print("The second file requested is the one with ~.fasta extension which contains the sequence list.")
print("Remember to use THE SAME fasta file used to get the tsv one.")
print("In the current folder you have the following *.fasta files:")
print_file_in_the_folder("*.fasta")

# *********************************************************************************************
# WHILE LOOP TO CHECK THE EXISTENCES OF THE INPUT FILE .fasta
# *********************************************************************************************
while True:
    fasta_file = input("Type the file name using this format -> file.fasta : ")
    if existence_file_check(fasta_file, "*.fasta") == True:
        break
    else:
        print(f"{fasta_file} doesn't exist or doesn't has .fasta extension. Retry.")
        pass

print(separator)

# *********************************************************************************************
# CHECK (AND EVENTUALLY ADD) IF THE FILE ALREADY HAS COLUMNS' NAME (0, 2, 3, ... )
# *********************************************************************************************
check_column_name(tsv_file)

# *********************************************************************************************
# CREATE WITH PANDAS A NEW DATAFRAME
# *********************************************************************************************
dataframe_file_tsv = pd.read_table(tsv_file)

# *********************************************************************************************
# COUNT HOW MANY RESULTS THERE ARE AND CHOOSE "Pfam" VS "SMART"
# *********************************************************************************************
result_of_analysis_pfam = dataframe_file_tsv.loc[dataframe_file_tsv["3"] == "Pfam"]
number_of_result_of_analysis_pfam = len(result_of_analysis_pfam)
result_of_analysis_smart = dataframe_file_tsv.loc[dataframe_file_tsv["3"] == "SMART"]
number_of_result_of_analysis_smart = len(result_of_analysis_smart)

if number_of_result_of_analysis_smart > number_of_result_of_analysis_pfam:
    result_of_analysis = result_of_analysis_smart
    analysis_used = "SMART"
else:
    result_of_analysis = result_of_analysis_pfam
    analysis_used = "Pfam"

number_of_result_of_analysis = int(len(result_of_analysis))

# *********************************************************************************************
# CREATE A DICTIONARY WITH THE RESULT OF ANALYSIS; THEN SORT IT
# *********************************************************************************************
unsorted_dictionary_of_result = result_of_analysis.to_dict("records")
sorted_results_dictionary = sorted(unsorted_dictionary_of_result, key=lambda i: (i["0"], i["6"]))

# *********************************************************************************************
# COUNTER TO RENAME OUTPUT FILE WHEN ANOTHER FILE WITH THE SAME NAME EXISTS
# *********************************************************************************************
list_of_file = os.listdir("./")
if "extracted_domains.fasta" in list_of_file:
    i = 1
    while os.path.exists("extracted_domains%s.fasta" % i):
        i += 1
else:
    i = ""

# *********************************************************************************************
# FOR EVERY ROW CONTAINING "Pfam" IN THE TSV FILE
# *********************************************************************************************
# er = Every Result
for er in range(0, number_of_result_of_analysis):
    # ----> EXTRACT MULTIPLE VARIABLE
    prot_accession = sorted_results_dictionary[er]["0"]
    seq_lenght = sorted_results_dictionary[er]["2"]
    signature_description = sorted_results_dictionary[er]["5"]
    start_location = sorted_results_dictionary[er]["6"]
    stop_location = sorted_results_dictionary[er]["7"]
    interpro_annotation = sorted_results_dictionary[er]["12"]

    # ----> USING pro_accession EXTRACT THE SEQUENCES AND SAVE IT IN seq_dominio USING (start/stop)_location
    with open(fasta_file) as elenco_fasta:
        for record in SeqIO.parse(elenco_fasta, "fasta"):
            if record.id == prot_accession:
                sequenza = f"{record.seq}"
    seq_dominio = sequenza[start_location-2:stop_location+2]

    # ----> IF OUTPUTFILE ALREADY EXISTS APPEND THE SEQUENCES REPORTING MULTIPLE VARIABLE FROM ABOVE
    try:
        with open("extracted_domains%s.fasta" % i, "a") as file_output:
            file_output.write(f">{prot_accession} - START: {start_location} - END: {stop_location} - {signature_description} - {interpro_annotation}")
            file_output.write("\n")
            file_output.write(seq_dominio)

    # ----> IF OUTPUTFILE DOES NOT EXISTA, THEN WE CREATE IT WITH THE FIRST SEQUENCE
    except FileNotFoundError:
        with open("extracted_domains%s.fasta" % i, "w") as file_output:
            file_output.write(f">{prot_accession} - START: {start_location} - END: {stop_location} - {signature_description} - {interpro_annotation}\n")
            file_output.write(seq_dominio)

# *********************************************************************************************
# CREATING A DICTIONARY WHICH IS GOING TO REPORT FOR EVERY DOMAIN HOW MUCH COPY OF IT THERE ARE
# *********************************************************************************************
domains_dict = {}
for er in range(0, number_of_result_of_analysis):
    signature_description = sorted_results_dictionary[er]["5"]
    if signature_description in domains_dict:
        domains_dict[signature_description] += 1
    else:
        domains_dict[signature_description] = 1

# *********************************************************************************************
# PRINT THE DOMAINS TABLE-GRID
# *********************************************************************************************
header = ("Domain name", "Domains' number found")
domains_tuple = sorted(domains_dict.items())
domains_tuple.insert(0, header)
print(tabulate(domains_tuple, tablefmt="grid", stralign="center"))

print(f"\n{analysis_used} analysis has been choosen (has more matches for this sequences).")

print(f"** {number_of_result_of_analysis} ** domain has been extracted and saved in extracted_domains%s.fasta\n" % i)
table_tsv_choice = input("Do you want to save this table as ~.tsv file? y/n ")
while True:
    if table_tsv_choice == "y":
        if "domains_list.fasta" in list_of_file:
            i = 1
            while os.path.exists("domains_list%s.fasta" % i):
                i += 1
        else:
            i = ""
        with open("domains_list%s.fasta" % i, "w") as domain_list:
            for everykey in domains_dict:
                domain_list.write("%s\t%s\n" % (everykey, domains_dict[everykey]))
            print(f"You can find your results in domains_list%s.fasta\n" % i)
        break
    elif table_tsv_choice == "n":
        break
    else:
        print("Strage way to type 'y' or 'n'. Retry.\n")

print(separator)

# *********************************************************************************************
# ASK FOR DRAW EVERY SEQUENCES (SEE DRAW.PY)
# *********************************************************************************************
while True:
    wanna_draw = input(f"Are you interested in create a new file.image for EACH sequence in {fasta_file}? y/n ")
    if wanna_draw == "y" and seq_in_fastafile_count(fasta_file) > 5:
        print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
        print(f"WARNING! In the {fasta_file} there are more than 5 sequences")
        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
        while True:
            choice = input("\nAre you sure to continue? y/n ")
            if choice == "y":
                sequences_drawer(fasta_file, tsv_file)
                break
            elif choice == "n":
                break
            else:
                print("Strage way to type 'y' or 'n'. Retry.\n")
        break
    elif wanna_draw == "y":
        sequences_drawer(fasta_file, tsv_file, analysis_used)
        break
    elif wanna_draw == "n":
        break
    else:
        print("Strage way to type 'y' or 'n'. Retry.\n")

print(separator)

# *********************************************************************************************
# BYE MESSAGE
# *********************************************************************************************
print("Have a productive day!")

print(separator)
