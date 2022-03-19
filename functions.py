import os
import fnmatch
from tabulate import tabulate
from Bio import SeqIO


# Create a file_list with all the file with the extension requested
# counter05 it is a counter for set the max number of element printed (by default: 6)
def print_file_in_the_folder(format_to_check):
    files_list = []
    for ognifile in os.listdir("./"):
        if fnmatch.fnmatch(ognifile, format_to_check):
            files_list.append(ognifile)
    stringa = ""
    counter05 = 0
    for n in files_list:
        a = f"[ {n} ]  "
        stringa += a
        counter05 += 1
        if counter05 > 6:
            break
    print(stringa)


# <return name_file in files_list> return TRUE if the input file name is in the files_list;
# otherwise return FALSE
def existence_file_check(name_file, format_to_check):
    files_list = []
    for everyfile in os.listdir("./"):
        if fnmatch.fnmatch(everyfile, format_to_check):
            files_list.append(everyfile)
    return name_file in files_list


def check_column_name(tsv_file):
    with open(tsv_file, "r") as file:
        copia = file.read()

    # Check -> If the first item of the list is "0" then it's already been added a numeric index
    check = copia[0]

    # WHY? If the 0\t1\t2\t3... is changed with  01-NameSeq\tmd5Seq... the first row of the first cell is used as index
    if check != "0":
        with open(tsv_file, "w") as file:
            file.write("0\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\n")
        with open(tsv_file, "a") as file:
            file.write(copia)


def seq_in_fastafile_count(fasta_file):
    with open(fasta_file, "r") as file:
        fileread = file.read()
        seq_counter = 0
        for everyline in fileread:
            if everyline.startswith(">"):
                seq_counter += 1
        return seq_counter


def printing_table(list_of_multiple_table_list):
    header = ("Accession ID", "Domain name", "Domains' number found")
    print(tabulate(list_of_multiple_table_list,
                   headers=header,
                   tablefmt="grid",
                   colalign=("center", "center", "center"),
                   showindex="always"
                   ))


# def domain_extraction(sorted_results_dictionary, er,
#                       domain_to_save, fasta_file,
#                       name_format, i):
#     prot_accession = sorted_results_dictionary[er]["0"]
#     seq_lenght = sorted_results_dictionary[er]["2"]
#     signature_description = sorted_results_dictionary[er]["5"]
#     start_location = sorted_results_dictionary[er]["6"]
#     stop_location = sorted_results_dictionary[er]["7"]
#     interpro_accession = sorted_results_dictionary[er]["11"]
#     interpro_annotation = sorted_results_dictionary[er]["12"]
#
#     if interpro_accession in domain_to_save:
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
#             name_format = "1,6,2,3,4,5"
#         name_format_dict = {
#             "1": prot_accession,
#             "2": start_location,
#             "3": stop_location,
#             "4": signature_description,
#             "5": interpro_annotation,
#             "6": domain_lenght,
#         }
#         name_format_choosen = name_format.split(",")
#         name_format_string = ">"
#         for n in name_format_choosen:
#             if n == "1":
#                 name_format_string += f" [{name_format_dict[n]}] -"
#             elif n == "2":
#                 name_format_string += f" [START: {name_format_dict[n]}] -"
#             elif n == "3":
#                 name_format_string += f" [STOP: {name_format_dict[n]}] -"
#             elif n == "4":
#                 name_format_string += f" [{name_format_dict[n]}] -"
#             elif n == "5":
#                 name_format_string += f" [{name_format_dict[n]}] -"
#             elif n == "6":
#                 name_format_string += f" [DOMAIN LENGTH: {name_format_dict[n]}] -"
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


