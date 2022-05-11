import os
import fnmatch
from tabulate import tabulate
from Bio import SeqIO
from datetime import date
import csv


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


def i_counter():
    # Set the date
    today = date.today()
    list_of_file = os.listdir("./")

    if "log.txt" in list_of_file:
        old_log = []
        with open("log.txt", "r") as file:
            everyline = csv.reader(file)
            for everyrow in everyline:
                old_log.append(everyrow)
        if old_log[len(old_log) - 1][0] == f"{today}_counter":
            i = int(old_log[len(old_log) - 1][1])
            i += 1
        else:
            i = 1
        with open("log.txt", "w") as file:
            counter = "counter"
            for everyitem in old_log:
                file.write(f"{everyitem[0]},{everyitem[1]}\n")
            file.write(f"{today}_{counter},{i}")
    else:
        with open("log.txt", "w") as file:
            i = 1
            counter = "counter"
            file.write(f"{today}_{counter},{i}")

    folder_name = f"{str(today)}_Analyis_number_{i}"
    os.mkdir(folder_name, 0o777)

    return folder_name


def seq_in_fastafile_count(fasta_file):
    with open(fasta_file, "r") as file:
        fileread = file.read()
        seq_counter = 0
        for everyline in fileread:
            if everyline.startswith(">"):
                seq_counter += 1
        return seq_counter


def protein_list_maker(fasta_file):
    temp_protein_list = []
    with open(fasta_file, "r") as file:
        for everyrecord in SeqIO.parse(file, "fasta"):
            if everyrecord.id in temp_protein_list:
                pass
            else:
                temp_protein_list.append(everyrecord.id)
    return temp_protein_list


def create_table_row_list(result_dictionary):
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
        temporary_list = [interpro_accession[everydomain], everydomain, domain_count_dict[everydomain]]
        table_row_list.append(temporary_list)

    table_row_list = sorted(table_row_list, key=lambda item: item[2], reverse=True)

    return table_row_list


def printing_table(table_list):
    header = ("Accession ID", "Domain name", "Domains' number found")
    print(tabulate(table_list,
                   headers=header,
                   tablefmt="grid",
                   colalign=("center", "center", "center"),
                   showindex="always"
                   ))


def top_five_domains(result_dictionary, everyprotein):
    domain_sorted_list = ""
    all_domains = {}
    for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:
        domain_name = everydomain["DOMAIN_NAME"]
        if domain_name in all_domains:
            all_domains[domain_name] += 1
        else:
            all_domains[domain_name] = 1

    all_domain_sorted = dict(sorted(all_domains.items(), key=lambda item: item[1], reverse=True))
    t_keys = list(all_domain_sorted.keys())

    for everyitem in t_keys:
        domain_sorted_list += f"\t\t\t\t<tr><td>{everyitem}</td><td>{all_domain_sorted[everyitem]}</td></tr>\n"

    return domain_sorted_list