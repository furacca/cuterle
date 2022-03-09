import os
import fnmatch
import pandas as pd
from Bio import SeqIO
import logo


def print_file_in_the_folder(format):
    files_list = []
    for ognifile in os.listdir("./"):
        if fnmatch.fnmatch(ognifile, format):
            files_list.append(ognifile)
    print(files_list)


def existence_file_check(name_file, format):
    files_list = []
    for everyfile in os.listdir("./"):
        if fnmatch.fnmatch(everyfile, format):
            files_list.append(everyfile)
    return name_file in files_list





def check_column_name(tsv_file):
    with open(tsv_file, "r") as file:
        copia = file.read()

    # Check -> se il primo valore della lista copia è 0 allora è già stata inserita una prima riga numerica
    check = copia[0]

    #  MA_CHE_CACTUS: se al posto del 0\t1\t2... inserisco 01-NomeSeq\tmd5Sequ... l'index delle righe non avviene e prende la stringa della prima cella per costruirlo
    if check != "0":
        with open(tsv_file, "w") as file:
            file.write("0\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\n")
        with open(tsv_file, "a") as file:
            file.write(copia)




