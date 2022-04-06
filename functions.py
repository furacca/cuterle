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


def i_counter():
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
    return i


def seq_in_fastafile_count(fasta_file):
    with open(fasta_file, "r") as file:
        fileread = file.read()
        seq_counter = 0
        for everyline in fileread:
            if everyline.startswith(">"):
                seq_counter += 1
        return seq_counter


def create_result_dictionary(protein_list, dataframe_tsv, prior_choice, fasta_file, domain_order):
    temporary_dictionary = {}
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
            continue

        with open(fasta_file) as elenco_fasta:
            for record in SeqIO.parse(elenco_fasta, "fasta"):
                if record.id == everyprotein:
                    protein_sequence = f"{record.seq}"

        if domain_order == "Increasing":
            reverse_value = False
        elif domain_order == "Decreasing":
            reverse_value = True

        # Result_of_analysis is a pandas dataframe
        # Sorting the list the dict by the START (found at index 6)
        unsorted_dict_result_filtered = result_of_analysis.to_dict("records")
        dict_result_filtered = sorted(unsorted_dict_result_filtered, key=lambda z: z["6"], reverse=reverse_value)

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
            domain_lenght = (stop_location+2) - (start_location-2)
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


        temporary_dictionary[everyprotein] = {
            "Domains_found": domain_counter,
            "Analysis_used": analysis_used,
            "Sequence": protein_sequence,
            "Extracted_domains": extracted_domain
        }

    return temporary_dictionary


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


def printing_table(list_of_multiple_table_list):
    header = ("Accession ID", "Domain name", "Domains' number found")
    print(tabulate(list_of_multiple_table_list,
                   headers=header,
                   tablefmt="grid",
                   colalign=("center", "center", "center"),
                   showindex="always"
                   ))


