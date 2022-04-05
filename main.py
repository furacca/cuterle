from functions import *
from drawer import *
from asciithing import *
from Bio import SeqIO
import pandas as pd
import os
import argparse
import textwrap

# Argparse - The raccomanded command-line parsing module in the python standard library
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
                            [optional] domains_list.csv - contains the table's raw data (domain_name,count)
                            [optional] domains_view[seq_name].jpg - schematic domains draw FOR EACH sequence
                            
                        NAME FORMAT
                            The name for every sequence added to extracted_domain.fasta is [>1,2,3,4,5,6]
                            
                            1 - Protein accession (e.g. P51587)
                            2 - Length of the domain
                            3 - Start location of the domain
                            4 - End location of the domain
                            5 - InterPro annotations - description (e.g. [BRCA2 repeat])
                            6 - InterPro accession (e.g. [IPR002035])
                            
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
# *********************************************************************************************

# # Get tsv file as input - The while loop checks the existences of the input tsv file
# if manual_mode and existence_file_check(tsv_file, "*.tsv"):
#     pass
# elif manual_mode and tsv_file is None:
#     print(f"You have not selected any tsv file!")
#     exit()
# elif manual_mode:
#     print(f"{tsv_file} doesn't exist or doesn't has the correct format!")
#     exit()
# elif manual_mode is False:
#     print(logo)
#     print(separator)
#     print("Welcome, this is CUTERLE, \n"
#           "a bioinformatic tool which return an output file containing every domain annotated by InterProScan\n"
#           "via Pfam or SMART analysis from the list of protein submitted.")
#     print(separator)
#     print("The first file requested is the one with ~.tsv extension which contains the domains coordinates.")
#     print("In the current folder you have the following *.tsv files:")
#     print_file_in_the_folder("*.tsv")
#
#     while True:
#         tsv_file = input("Type the file name using this format -> file.tsv : ")
#         if existence_file_check(tsv_file, "*.tsv"):
#             break
#         else:
#             print(f"{tsv_file} doesn't exist or doesn't has .tsv extension. Retry.")
#             pass
#
# # Get fasta file as input - The while loop checks the existences of the input fasta file
# if manual_mode and existence_file_check(tsv_file, "*.fasta"):
#     pass
# elif manual_mode and fasta_file is None:
#     print(f"You have not selected any fasta file!")
#     exit()
# elif manual_mode:
#     print(f"{fasta_file} doesn't exist or doesn't has the correct format!")
#     exit()
# else:
#     print(separator)
#     print("The second file requested is the one with ~.fasta extension which contains the sequence list.")
#     print("Remember to use THE SAME fasta file used to get the tsv one.")
#     print("In the current folder you have the following *.fasta files:")
#     print_file_in_the_folder("*.fasta")
#     while True:
#         fasta_file = input("Type the file name using this format -> file.fasta : ")
#         if existence_file_check(fasta_file, "*.fasta"):
#             break
#         else:
#             print(f"{fasta_file} doesn't exist or doesn't has .fasta extension. Retry.")
#             pass


# The "i" set the same number-counter for all output file (extracted_files, table, log, ecc),
# avoiding overwrite some file previously created
i = i_counter()

tsv_file = "a.tsv"
fasta_file = "a.fasta"

# Checks (and eventually add) if the tsv file already has columns' name (0, 1, 2, 3, ...)
check_column_name(tsv_file)

# Create a list which contains every protein name
protein_list = []
with open(fasta_file, "r") as file:
    for everyrecord in SeqIO.parse(file, "fasta"):
        if everyrecord.id in protein_list:
            pass
        else:
            protein_list.append(everyrecord.id)

# Create with pandas a new dataframe
dataframe_tsv = pd.read_table(tsv_file)

# Create results_dictionary
result_dictionary = create_result_dictionary(protein_list, dataframe_tsv, prior_choice, fasta_file)

# Count how many result for each analysis have been found
smart_counter = 0
pfam_counter = 0
for everyrecord in result_dictionary:
    if result_dictionary[everyrecord]["Analysis_used"] == "Pfam":
        pfam_counter += len(result_dictionary[everyrecord]["Extracted_domains"])
    elif result_dictionary[everyrecord]["Analysis_used"] == "SMART":
        pfam_counter += len(result_dictionary[everyrecord]["Extracted_domains"])

# Count how many result there are in total for both analysis
smart_plus_pfam = smart_counter + pfam_counter
table_list = create_table_row_list(result_dictionary)



if manual_mode and table_choice:
    with open("domains_list%s.csv" % i, "w") as domain_csv:
        for everyrow in table_list:
            domain_csv.write(f"{everyrow[0]},{everyrow[1]},{everyrow[2]}\n")

save_choice_list = []
domain_to_save = []
if manual_mode and accession:
    save_choice_list = accession.split(",")
    for everyaccession in table_list:
        domain_to_save.append(everyaccession)

    if accession:
        save_choice_list = accession.split(",")
        for everyaccession in save_choice_list:
            domain_to_save.append(everyaccession)
else:
    for everyprotein in protein_list:
        for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:
            ip_accession = everydomain["IP_ACCESSION"]
            if ip_accession in domain_to_save:
                pass
            else:
                domain_to_save.append(everydomain["IP_ACCESSION"])

# else:
# printing_table(table_list)
# print(f"SMART results: {smart_counter}")
# print(f"PFAM results: {pfam_counter}")
#     print(separator)
#     printing_table(list_of_multiple_table_list)
#     print(f"\nThere was {len(result_of_analysis_pfam)} Pfam results vs {len(result_of_analysis_smart)} SMART results.")
#     print(f"{analysis_used} analysis has been chosen.")
#
#     while True:
#         table_choice = input("Do you want to save this table as ~.csv file? y/n ")
#         if table_choice == "y":
#             with open("domains_list%s.csv" % i, "w") as domain_csv:
#                 for everykey in domains_counter_dict:
#                     domain_csv.write("%s,%s\n" % (everykey, domains_counter_dict[everykey]))
#                 print(f"You can find your results in domains_list%s.csv\n" % i)
#             break
#         elif table_choice == "n":
#             break
#         else:
#             print("Strange way to type 'y' or 'n'. Retry.\n")
#
#     print("\nWhich domains do you want to save?")
#     print("- Save all the domains -> 'all'")
#     print("- Choose by index -> e.g. single 'index,1' or multiple 'index,1,3,4'")
#     print("- None -> 'none' ")
#     print("DO NOT use space. If you have some doubt, go back to the readme.")
#
#     while True:
#         save_choice_input = input("Write here your choice: ")
#         save_choice_list = save_choice_input.split(",")
#         save_choice = save_choice_list[0]
#
#         if save_choice == "index":
#             for everychoice in save_choice_list:
#                 if everychoice == "index":
#                     pass
#                 else:
#                     domain_to_save.append(list_of_multiple_table_list[int(everychoice)][0])
#             break
#         elif save_choice == "all":
#             for everychoice in range(0, len(list_of_multiple_table_list)):
#                 if everychoice == "all":
#                     pass
#                 else:
#                     domain_to_save.append(list_of_multiple_table_list[int(everychoice)][0])
#             break
#         elif save_choice == "none":
#             break
#         else:
#             print("You forgot to add 'index' or 'accession', or made some typos. Retry.\n")
#



# # *********************************************************************************************
# # SAVING THE DOMAINS
# # *********************************************************************************************

# Counter for the domain saved
domain_saved = 0

#  er = every result
for everyprotein in protein_list:
    for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:
        protein_accession = everyprotein
        domain_name = everydomain["DOMAIN_NAME"]
        domain_order = everydomain["DOMAIN_ORDER"]
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

        # ----> Renaming the sequence following the input
        if name_format is None:
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

        domain_saved += 1

if manual_mode is False:
    print(f"\n{domain_saved} domains had been saved in extracted_domains{i}.fasta")
#
# # *********************************************************************************************
# # ASK FOR DRAW EVERY SEQUENCES (SEE DRAW.PY)
# # *********************************************************************************************
# if manual_mode:
#     if draw_choice:
#         sequences_drawer(fasta_file, domains_counter_dict, tsv_file, analysis_used, column_with_description)
# else:
#     print(separator)
#     while True:
#         wanna_draw = input(f"Are you interested in create a new file.image for EACH sequence in {fasta_file}? y/n ")
#         if wanna_draw == "y" and seq_in_fastafile_count(fasta_file) > 5:
#             print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
#             print(f"WARNING! In the {fasta_file} there are more than 5 sequences")
#             print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
#             while True:
#                 choice = input("\nAre you sure to continue? y/n ")
#                 if choice == "y":
#                     sequences_drawer(fasta_file, domains_counter_dict, tsv_file, analysis_used, column_with_description)
#                     break
#                 elif choice == "n":
#                     break
#                 else:
#                     print("Strange way to type 'y' or 'n'. Retry.\n")
#             break
#         elif wanna_draw == "y":
#             sequences_drawer(fasta_file, domains_counter_dict, tsv_file, analysis_used, column_with_description)
#             break
#         elif wanna_draw == "n":
#             break
#         else:
#             print("Strange way to type 'y' or 'n'. Retry.\n")
#
#     print(separator)
#
# *********************************************************************************************
# BYE MESSAGE
# *********************************************************************************************
# if manual_mode:
#     pass
# else:
#     print("Have a productive day!")
#     print(separator)
