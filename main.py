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
result_dictionary = {}

# Count how many domains have been extracted
global_domain_counter = 0

for everyprotein in protein_list:
    # Reset the domain counter
    domain_counter = 0
    result_of_analysis = ""
    do = 0
    extracted_domain = []

    # Grouping all PFAM results for every protein (.loc[] returns a group of rows and columns by label)
    pfam_result = dataframe_tsv.loc[dataframe_tsv["3"] == "Pfam"]
    pfam_result_for_everyprotein = pfam_result.loc[dataframe_tsv["0"] == everyprotein]

    # Count how many results there are for PFAM for each protein
    number_of_result_of_analysis_pfam = len(pfam_result_for_everyprotein)

    # Grouping all SMART results for every protein (.loc[] returns a group of rows and columns by label)
    smart_result = dataframe_tsv.loc[dataframe_tsv["3"] == "smart"]
    smart_result_for_everyprotein = smart_result.loc[dataframe_tsv["0"] == everyprotein]

    # Count how many results there are for SMART for each protein
    number_of_result_of_analysis_smart = len(smart_result_for_everyprotein)

    # Check if there are a prior choose made and set the correct table (filter applied) from which get the data
    analysis_used = ""
    if prior_choice == "SMART":
        analysis_used = "SMART"
        domain_counter = number_of_result_of_analysis_smart
        result_of_analysis = smart_result_for_everyprotein
    elif prior_choice == "Pfam":
        analysis_used = "Pfam"
        domain_counter = number_of_result_of_analysis_pfam
        result_of_analysis = pfam_result_for_everyprotein
    elif number_of_result_of_analysis_smart > number_of_result_of_analysis_pfam:
        analysis_used = "SMART"
        domain_counter = number_of_result_of_analysis_smart
        result_of_analysis = smart_result_for_everyprotein
    elif number_of_result_of_analysis_smart <= number_of_result_of_analysis_pfam:
        analysis_used = "Pfam"
        domain_counter = number_of_result_of_analysis_pfam
        result_of_analysis = pfam_result_for_everyprotein
    elif number_of_result_of_analysis_pfam + number_of_result_of_analysis_smart == 0:
        # If the protein hasn't ANY domains, skip it (avoiding error)
        pass

    global_domain_counter += domain_counter

    # Result_of_analysis is a pandas dataframe
    # Sorting the list the dict by the START (found at index 6)
    unsorted_dict_result_filtered = result_of_analysis.to_dict("records")
    dict_result_filtered = sorted(unsorted_dict_result_filtered, key=lambda z: z["6"], reverse=False)

    # Set the right column to use
    column_with_description = ""
    if analysis_used == "SMART":
        column_with_description = "12"
    elif analysis_used == "Pfam":
        column_with_description = "5"

    # er = every result
    for er in range(0, domain_counter):
        # do = domain order
        do += 1
        domain_key = int(f"{do}")

        # Extract multiple variable
        domain_name = dict_result_filtered[er][column_with_description]
        start_location = dict_result_filtered[er]["6"]
        stop_location = dict_result_filtered[er]["7"]
        domain_lenght = stop_location - start_location
        interpro_accession = dict_result_filtered[er]["11"]

        name_format_dict = {
            "DOMAIN_NAME": domain_name,
            "DOMAIN_ORDER": domain_key,
            "START": start_location,
            "STOP": stop_location,
            "LENGTH": domain_lenght,
            "IP_ACCESSION": interpro_accession,
        }

        extracted_domain.append(name_format_dict)

    # {"domains_number":domain_counter}
    result_dictionary[everyprotein] = {
        "Domains_found": domain_counter,
        "Analysis_used": analysis_used,
        "Extracted_domains": extracted_domain
    }


# Count how many result for each analysis have been found
smart_counter = 0
pfam_counter = 0
for everyrecord in result_dictionary:

    if result_dictionary[everyrecord]["Analysis_used"] == "Pfam":
        pfam_counter += len(result_dictionary[everyrecord]["Extracted_domains"])
    elif result_dictionary[everyrecord]["Analysis_used"] == "SMART":
        pfam_counter += len(result_dictionary[everyrecord]["Extracted_domains"])

print(f"SMART results: {smart_counter}")
print(f"PFAM results: {pfam_counter}")

# Create a list containing all the row printed by the table
table_row_list = []

domain_count_dict = {}
interpro_accession = {}

for everyrecord in result_dictionary:
    for n in result_dictionary[everyrecord]["Extracted_domains"]:
        domain_name = n["DOMAIN_NAME"]
        ip_accession = n["IP_ACCESSION"]

        if domain_name in domain_count_dict:
            domain_count_dict[domain_name] += 1
        else:
            domain_count_dict[domain_name] = 1

        if ip_accession in interpro_accession:
            pass
        else:
            interpro_accession[domain_name] = ip_accession

for everydomain in interpro_accession:
    temporary_list = []
    temporary_list.append(interpro_accession[everydomain])
    temporary_list.append(everydomain)
    temporary_list.append(domain_count_dict[everydomain])
    table_row_list.append(temporary_list)

table_row_list = sorted(table_row_list, key=lambda item: item[2], reverse=True)

printing_table(table_row_list)





# # *********************************************************************************************
# # PRINT THE DOMAINS TABLE-GRID
# # *********************************************************************************************
# list_of_multiple_table_list = []
#
# for n in domains_counter_dict:
#     one_row_list = []
#
#     for m in domains_interpro_accession_dict:
#         if n == m:
#             one_row_list.append(domains_interpro_accession_dict[m])
#
#     one_row_list.append(n)
#     one_row_list.append(domains_counter_dict[n])
#     list_of_multiple_table_list.append(one_row_list)
#
# list_of_multiple_table_list = sorted(list_of_multiple_table_list, key=lambda item: item[2], reverse=True)
#
# domain_to_save = []
# save_choice_list = []
#
# if manual_mode:
#     if table_choice:
#         with open("domains_list%s.csv" % i, "w") as domain_csv:
#             for everykey in domains_counter_dict:
#                 domain_csv.write("%s,%s\n" % (everykey, domains_counter_dict[everykey]))
#     if accession:
#         save_choice_list = accession.split(",")
#         for everychoice in save_choice_list:
#             domain_to_save.append(everychoice)
#     else:
#         for everychoice in range(0, len(list_of_multiple_table_list)):
#             domain_to_save.append(list_of_multiple_table_list[int(everychoice)][0])
# else:
#     print(separator)
#
#     printing_table(list_of_multiple_table_list)
#
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
#
# # *********************************************************************************************
# # SAVING THE DOMAINS
# # *********************************************************************************************
# # er = Every Result
# domain_saved = 0
# for er in range(0, number_of_result_of_analysis):
#     # ----> EXTRACT MULTIPLE VARIABLE
#     prot_accession = sorted_results_dictionary[er]["0"]
#     seq_lenght = sorted_results_dictionary[er]["2"]
#     signature_description = sorted_results_dictionary[er]["5"]
#     start_location = sorted_results_dictionary[er]["6"]
#     stop_location = sorted_results_dictionary[er]["7"]
#     interpro_accession = sorted_results_dictionary[er]["11"]
#     interpro_annotation = sorted_results_dictionary[er]["12"]
#
#     if interpro_accession in domain_to_save:
#         domain_saved += 1
#         # ----> USING pro_accession EXTRACT THE SEQUENCES AND SAVE IT IN seq_dominio USING (start/stop)_location
#         with open(fasta_file) as elenco_fasta:
#             for record in SeqIO.parse(elenco_fasta, "fasta"):
#                 if record.id == prot_accession:
#                     sequenza = f"{record.seq}"
#         seq_dominio = sequenza[start_location-2:stop_location+2]
#         domain_lenght = (stop_location+2)-(start_location-2)
#
#         # ----> Renaming the sequence following the input
#         if name_format is None:
#             name_format = "1,2,3,4,5,6"
#
#         name_format_dict = {
#             "1": prot_accession,
#             "2": domain_lenght,
#             "3": start_location,
#             "4": stop_location,
#             "5": signature_description,
#             "6": interpro_accession,
#         }
#
#         name_format_choosen = name_format.split(",")
#         name_format_string = ">"
#
#         for n in name_format_choosen:
#             if n == "1":
#                 name_format_string += f" [{name_format_dict[n]}] -"
#             elif n == "2":
#                 name_format_string += f" [DOMAIN LENGTH: {name_format_dict[n]}] -"
#             elif n == "3":
#                 name_format_string += f" [START: {name_format_dict[n]}] -"
#             elif n == "4":
#                 name_format_string += f" [STOP: {name_format_dict[n]}] -"
#             elif n == "5":
#                 name_format_string += f" [{name_format_dict[n]}] -"
#             elif n == "6":
#                 name_format_string += f" [{name_format_dict[n]}] -"
#
#         length_name_format_final = len(name_format_string)
#         sliced_text = slice(length_name_format_final - 2)
#         name_format_string_final = name_format_string[sliced_text]
#
#         # ----> IF OUTPUTFILE ALREADY EXISTS APPEND THE SEQUENCES REPORTING MULTIPLE VARIABLE FROM ABOVE
#         try:
#             with open("extracted_domains%s.fasta" % i, "a") as file_output:
#                 file_output.write(f"{name_format_string_final}\n")
#                 file_output.write(f"{seq_dominio}\n\n")
#
#         # ----> IF OUTPUTFILE DOES NOT EXIST, THEN WE CREATE IT WITH THE FIRST SEQUENCE
#         except FileNotFoundError:
#             with open("extracted_domains%s.fasta" % i, "w") as file_output:
#                 file_output.write(f"{name_format_string_final}\n")
#                 file_output.write(f"{seq_dominio}\n\n")
#
# if manual_mode is False:
#     print(f"\n{domain_saved} domains had been saved in extracted_domains{i}.fasta")
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
# # *********************************************************************************************
# # BYE MESSAGE
# # *********************************************************************************************
# if manual_mode:
#     pass
# else:
#     print("Have a productive day!")
#     print(separator)
