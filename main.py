from functions import *
from drawer import *
from asciithing import *
from Bio import SeqIO
import pandas as pd
import os
import argparse
import textwrap

# *********************************************************************************************
# ARGPARSE - THE RACCOMENDED COMMAND-LINE PARSING MODULE IN THE PYTHON STANDARD LIBRARY
# *********************************************************************************************

description_message = '''\
                        -----------------------------------------------------------------
                        IF NO OPTION IS SELECTED, THE PROGRAM WILL RUN IN [ASSISTED MODE]
                        -----------------------------------------------------------------
                        DESCRIPTION

                            Cuterle is a bioinformatic tool.
                            It returns an output file containing every domain annotated by InterProScan.
                            Pfam or SMART analysis are choosen by which method has more matches.


                        LIST OF OUTPUT FILE

                            extracted_domains.fasta - contains every domains extracted
                            [optional] domains_list.fasta - contains every kind of domains extracted, sort by matches
                            [optional] domains_view[seq_name].jpg - schematic domains draw FOR EACH sequence
                            
                        NAME FORMAT
                            The name for every sequence added to extracted_domain.fasta is [>1,2,3,4,5]
                            
                            1 - Protein accession (e.g. P51587)
                            2 - Start location of the domain
                            3 - End location of the domain
                            4 - Signature accession (e.g. PF09103 / G3DSA:2.40.50.140)
                            5 - InterPro annotations - description (e.g. BRCA2 repeat)
                            
                            It is possible to CHANGE the order for every tag;
                                e.g. [-nf 1] or [-nf 1,2,3,4] or [-nf 5,4,3,2,2,2,1]
                            DO NOT USE SPACE between the number!
                        ------------------------------------------
                      '''

cuterle_parser = argparse.ArgumentParser(usage="%(prog)s  [options]",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(description_message)
                                         )

cuterle_parser.add_argument("-m",
                            help="Enable the manual mode. -tsv and -fasta argument are requested",
                            action="store_true"
                            )

cuterle_parser.add_argument("-tsv",
                            help="Input file containing the tsv file output from InterPro",
                            type=str,
                            metavar="file.tsv"
                            )

cuterle_parser.add_argument("-fasta",
                            help="Input file containing the fasta sequences",
                            type=str,
                            metavar="file.fasta"
                            )

cuterle_parser.add_argument("-a",
                            help="Prior choice between 'Pfam' and 'SMART'. Read the documentation.",
                            type=str,
                            metavar="Pfam or SMART"
                            )

cuterle_parser.add_argument("-nf",
                            help="Name format. Read the documentation. Format: [1,2,3,4,5]",
                            type=str,
                            )

cuterle_parser.add_argument("-accession",
                            help="InterPro annotations - accession ((e.g. IPR002093)",
                            type=str,
                            )

cuterle_parser.add_argument("-savetable",
                            help="Export all kind of domains extracted in ~.csv file, sort by matches",
                            action="store_true"
                            )

cuterle_parser.add_argument("-draw_image",
                            help="FOR EACH sequences create a ~.jpg file reporting sequence+domains",
                            action="store_true"
                            )

cuterle_options = cuterle_parser.parse_args()

manual_mode = cuterle_options.m
tsv_file = cuterle_options.tsv
fasta_file = cuterle_options.fasta
prior_choice = cuterle_options.a
name_format = cuterle_options.nf
accession = cuterle_options.accession
table_choice = cuterle_options.savetable
draw_choice = cuterle_options.draw_image

# *********************************************************************************************
# START
# *********************************************************************************************
if manual_mode:
    pass
else:
    print(logo)
    print(separator)
    print("Welcome, this is CUTERLE, \n"
          "a bioinformatic tool which return an output file containing every domain annotated by InterProScan\n"
          "via Pfam or SMART analysis from the list of protein submitted.")

# *********************************************************************************************
# GIVE THE TSV FILE AS INPUT - THE WHILE LOOP CHECKS THE EXISTENCES OF THE INPUT FILE .tsv
# *********************************************************************************************
if manual_mode:
    if existence_file_check(tsv_file, "*.tsv"):
        pass
    else:
        if tsv_file is None:
            print(f"You have not selected any tsv file!")
        else:
            print(f"{tsv_file} doesn't exist or doesn't has the correct format!")
        exit()
else:
    print(separator)
    print("The first file requested is the one with ~.tsv extension which contains the domains coordinates.")
    print("In the current folder you have the following *.tsv files:")
    print_file_in_the_folder("*.tsv")

    while True:
        tsv_file = input("Type the file name using this format -> file.tsv : ")
        if existence_file_check(tsv_file, "*.tsv"):
            break
        else:
            print(f"{tsv_file} doesn't exist or doesn't has .tsv extension. Retry.")
            pass

# *********************************************************************************************
# GIVE THE FASTA FILE AS INPUT - THE WHILE LOOP CHECKS THE EXISTENCES OF THE INPUT FILE .fasta
# *********************************************************************************************
if manual_mode:
    if existence_file_check(fasta_file, "*.fasta"):
        pass
    else:
        if fasta_file is None:
            print(f"You have not selected any fasta file!")
        else:
            print(f"{fasta_file} doesn't exist or doesn't has the correct format!")
        exit()
else:
    print(separator)
    print("The second file requested is the one with ~.fasta extension which contains the sequence list.")
    print("Remember to use THE SAME fasta file used to get the tsv one.")
    print("In the current folder you have the following *.fasta files:")
    print_file_in_the_folder("*.fasta")

    while True:
        fasta_file = input("Type the file name using this format -> file.fasta : ")
        if existence_file_check(fasta_file, "*.fasta"):
            break
        else:
            print(f"{fasta_file} doesn't exist or doesn't has .fasta extension. Retry.")
            pass


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

analysis_used = ""
# Check if a prior_choice has been made, otherwise count the result and proceed
if prior_choice == "SMART":
    analysis_used = "SMART"
elif prior_choice == "Pfam":
    analysis_used = "Pfam"
elif number_of_result_of_analysis_smart > number_of_result_of_analysis_pfam:
    analysis_used = "SMART"
elif number_of_result_of_analysis_smart <= number_of_result_of_analysis_pfam:
    analysis_used = "Pfam"

result_of_analysis = ""
if analysis_used == "Pfam":
    result_of_analysis = result_of_analysis_pfam
elif analysis_used == "SMART":
    result_of_analysis = result_of_analysis_smart

number_of_result_of_analysis = int(len(result_of_analysis))

# *********************************************************************************************
# CREATE A DICTIONARY WITH THE RESULT OF ANALYSIS; THEN SORT IT
# *********************************************************************************************
unsorted_dictionary_of_result = result_of_analysis.to_dict("records")
sorted_results_dictionary = sorted(unsorted_dictionary_of_result, key=lambda z: (z["0"], z["6"]))

# *********************************************************************************************
# CREATING TWO NEW DICTIONARIES:
# 1) domains_counter_dict which report for every domain how much copy of it there are
# 2) domains_interpro_accession_dict which report for every domain the InterPro accession ID
# *********************************************************************************************
column_with_description = ""
if analysis_used == "SMART":
    column_with_description = "12"
elif analysis_used == "Pfam":
    column_with_description = "5"

domains_counter_dict = {}
domains_interpro_accession_dict = {}
for er in range(0, number_of_result_of_analysis):
    signature_description = sorted_results_dictionary[er][column_with_description]

    if signature_description in domains_counter_dict:
        domains_counter_dict[signature_description] += 1
    else:
        domains_counter_dict[signature_description] = 1

    interpro_accession = sorted_results_dictionary[er]["11"]

    if interpro_accession in domains_interpro_accession_dict:
        pass
    elif interpro_accession not in domains_interpro_accession_dict:
        domains_interpro_accession_dict[signature_description] = interpro_accession

# *********************************************************************************************
# THE i COUNTER SET THE SAME NUMBER FOR ALL OUTPUT FILE, AVOIDING OVERWRITE SOME FILE PREVIOUSLY CREATED
# *********************************************************************************************
list_of_file = os.listdir("./")

if "extracted_domains.fasta" in list_of_file \
        or "domains_table.csv" in list_of_file \
        or "domains_list.csv" in list_of_file:
    i = 1
    while os.path.exists("extracted_domains%s.fasta" % i):
        i += 1
    while os.path.exists("domains_table%s.csv" % i):
        i += 1
    while os.path.exists("domains_list%s.csv" % i):
        i += 1
else:
    i = ""

# *********************************************************************************************
# PRINT THE DOMAINS TABLE-GRID
# *********************************************************************************************
list_of_multiple_table_list = []

for n in domains_counter_dict:
    one_row_list = []

    for m in domains_interpro_accession_dict:
        if n == m:
            one_row_list.append(domains_interpro_accession_dict[m])

    one_row_list.append(n)
    one_row_list.append(domains_counter_dict[n])
    list_of_multiple_table_list.append(one_row_list)

list_of_multiple_table_list = sorted(list_of_multiple_table_list, key=lambda item: item[2], reverse=True)

domain_to_save = []

if manual_mode:
    if table_choice:
        with open("domains_list%s.csv" % i, "w") as domain_list:
            for everykey in domains_counter_dict:
                domain_list.write("%s,%s\n" % (everykey, domains_counter_dict[everykey]))
    if accession != "":
        save_choice_list = accession.split(",")
        for everychoice in save_choice_list:
            domain_to_save.append(everychoice)
else:
    print(separator)

    printing_table(list_of_multiple_table_list)

    print(f"\nThere was {len(result_of_analysis_pfam)} Pfam results vs {len(result_of_analysis_smart)} results.")
    print(f"{analysis_used} analysis has been chosen.")

    table_choice = input("Do you want to save this table as ~.csv file? y/n ")

    while True:
        if table_choice == "y":
            with open("domains_list%s.csv" % i, "w") as domain_list:
                for everykey in domains_counter_dict:
                    domain_list.write("%s,%s\n" % (everykey, domains_counter_dict[everykey]))
                print(f"You can find your results in domains_list%s.csv\n" % i)
            break
        elif table_choice == "n":
            break
        else:
            print("Strange way to type 'y' or 'n'. Retry.\n")

    print("\nWhich domains do you want to save?")
    print("- Save all the domains -> 'all'")
    print("- Choose by index -> e.g. single 'index,1' or multiple 'index,1,3,4'")
    print("DO NOT use space. If you have some doubt, go back to the readme.")

    while True:
        save_choice_input = input("Write here your choice: ")
        save_choice_list = save_choice_input.split(",")
        save_choice = save_choice_list[0]

        if save_choice == "index":
            for everychoice in save_choice_list:
                if everychoice == "index":
                    pass
                else:
                    domain_to_save.append(list_of_multiple_table_list[int(everychoice)][0])
            break
        elif save_choice == "all":
            for everychoice in range(0, len(list_of_multiple_table_list)):
                if everychoice == "all":
                    pass
                else:
                    domain_to_save.append(list_of_multiple_table_list[int(everychoice)][0])
            break
        else:
            print("You forgot to add 'index' or 'accession', or made some typos. Retry.\n")


# *********************************************************************************************
# SAVING THE DOMAINS
# *********************************************************************************************
# er = Every Result
domain_saved = 0
for er in range(0, number_of_result_of_analysis):
    # ----> EXTRACT MULTIPLE VARIABLE
    prot_accession = sorted_results_dictionary[er]["0"]
    seq_lenght = sorted_results_dictionary[er]["2"]
    signature_description = sorted_results_dictionary[er]["5"]
    start_location = sorted_results_dictionary[er]["6"]
    stop_location = sorted_results_dictionary[er]["7"]
    interpro_accession = sorted_results_dictionary[er]["11"]
    interpro_annotation = sorted_results_dictionary[er]["12"]

    if interpro_accession in domain_to_save:
        # ----> USING pro_accession EXTRACT THE SEQUENCES AND SAVE IT IN seq_dominio USING (start/stop)_location
        with open(fasta_file) as elenco_fasta:
            for record in SeqIO.parse(elenco_fasta, "fasta"):
                if record.id == prot_accession:
                    sequenza = f"{record.seq}"
        seq_dominio = sequenza[start_location-2:stop_location+2]
        domain_lenght = (stop_location+2)-(start_location-2)
        # ----> Renaming the sequence following the input
        if name_format is None:
            name_format = "1,6,2,3,4,5"
        name_format_dict = {
            "1": prot_accession,
            "2": start_location,
            "3": stop_location,
            "4": signature_description,
            "5": interpro_annotation,
            "6": domain_lenght,
        }
        name_format_choosen = name_format.split(",")
        name_format_string = ">"
        for n in name_format_choosen:
            if n == "1":
                name_format_string += f" [{name_format_dict[n]}] -"
            elif n == "2":
                name_format_string += f" [START: {name_format_dict[n]}] -"
            elif n == "3":
                name_format_string += f" [STOP: {name_format_dict[n]}] -"
            elif n == "4":
                name_format_string += f" [{name_format_dict[n]}] -"
            elif n == "5":
                name_format_string += f" [{name_format_dict[n]}] -"
            elif n == "6":
                name_format_string += f" [DOMAIN LENGTH: {name_format_dict[n]}] -"

        length_name_format_final = len(name_format_string)
        sliced_text = slice(length_name_format_final - 2)
        name_format_string_final = name_format_string[sliced_text]

        # ----> IF OUTPUTFILE ALREADY EXISTS APPEND THE SEQUENCES REPORTING MULTIPLE VARIABLE FROM ABOVE
        try:
            with open("extracted_domains%s.fasta" % i, "a") as file_output:
                file_output.write(f"{name_format_string_final}\n")
                file_output.write(f"{seq_dominio}\n\n")

        # ----> IF OUTPUTFILE DOES NOT EXIST, THEN WE CREATE IT WITH THE FIRST SEQUENCE
        except FileNotFoundError:
            with open("extracted_domains%s.fasta" % i, "w") as file_output:
                file_output.write(f"{name_format_string_final}\n")
                file_output.write(f"{seq_dominio}\n\n")
        domain_saved += 1

print(f"\n{domain_saved} domains had been saved in extracted_domains{i}.fasta")

# *********************************************************************************************
# ASK FOR DRAW EVERY SEQUENCES (SEE DRAW.PY)
# *********************************************************************************************
if manual_mode:
    if draw_choice:
        sequences_drawer(fasta_file, domains_counter_dict, tsv_file, analysis_used, column_with_description)
else:
    print(separator)
    while True:
        wanna_draw = input(f"Are you interested in create a new file.image for EACH sequence in {fasta_file}? y/n ")
        if wanna_draw == "y" and seq_in_fastafile_count(fasta_file) > 5:
            print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
            print(f"WARNING! In the {fasta_file} there are more than 5 sequences")
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
            while True:
                choice = input("\nAre you sure to continue? y/n ")
                if choice == "y":
                    sequences_drawer(fasta_file, domains_counter_dict, tsv_file, analysis_used, column_with_description)
                    break
                elif choice == "n":
                    break
                else:
                    print("Strange way to type 'y' or 'n'. Retry.\n")
            break
        elif wanna_draw == "y":
            sequences_drawer(fasta_file, domains_counter_dict, tsv_file, analysis_used, column_with_description)
            break
        elif wanna_draw == "n":
            break
        else:
            print("Strange way to type 'y' or 'n'. Retry.\n")

    print(separator)

# *********************************************************************************************
# BYE MESSAGE
# *********************************************************************************************
if manual_mode:
    pass
else:
    print("Have a productive day!")
    print(separator)
