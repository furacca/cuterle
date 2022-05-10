import pdfkit
from functions import *

text = ""


def html_body(fasta_file, tsv_file, result_dictionary, table_list):
    global text
    # Counting the number of sequences
    keys = result_dictionary.keys()
    number_of_sequeces = 0
    for everykey in keys:
        number_of_sequeces += 1

    # Using "s" it there are two or more sequences
    plural = "s"
    if number_of_sequeces == 1 or number_of_sequeces == 0:
        plural = ""

    # Counting the number of domains
    number_of_domains = 0
    for everyrow in table_list:
        number_of_domains += everyrow[2]

    # Create one row (in a html table) for every domain
    # Structure: [IP_ACCESSION | DOMAIN_NAME | COUNTER]
    one_line_for_every_domain = ''''''

    for everyrow in table_list:
        one_line_for_every_domain += f'''\n\t\t\t\t<tr><td>{everyrow[0]}</td><td>{everyrow[1]}</td><td>{everyrow[2]}</td></tr>'''


    protein_list_html = protein_list_maker(fasta_file)
    single_protein_information = '''
    '''

    for everyprotein in protein_list_html:

        t_domains_found = result_dictionary[everyprotein]["Domains_found"]
        t_sequence_len = len(result_dictionary[everyprotein]["Sequence"])
        single_protein_information += f'''
        \n\t\t\t
        <details open>
        <summary style="display: flex; cursor: pointer; background:lightgray;">
        <b>{everyprotein}</b>
        </summary>
        <table>
        <tr><td> Sequence name: </td><td>{everyprotein}</td></tr>
        <tr><td> Length: </td><td>{t_sequence_len}</td></tr>
        <tr><td> Domains found: </td><td>{t_domains_found}</td></tr>
        </table>
        <details>
        <summary style="display: flex; cursor: pointer;">
        <i>Click me for detailed information about domains</i>
        </summary>
        <table>'''

        domains_dict = {}
        for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:
            protein_accession = everyprotein
            t_domain_name = everydomain["DOMAIN_NAME"]
            t_domain_order = everydomain["DOMAIN_ORDER"]
            t_start_location = everydomain["START"]
            t_stop_location = everydomain["STOP"]
            t_domain_length = everydomain["LENGTH"]
            t_ip_accession = everydomain["IP_ACCESSION"]
            t_protein_sequence = result_dictionary[everyprotein]["Sequence"]
            t_domain_sequence = t_protein_sequence[t_start_location:t_stop_location]

            single_protein_information += f'''
            <tr><td>Domain name: </td><td>{t_domain_name}</td></tr>
            <tr><td>Domain order: </td><td>{t_domain_order}</td></tr>
            <tr><td>Domain length: </td><td>{t_domain_length}</td></tr>
            <tr><td>Start location: </td><td>{t_start_location}</td></tr>
            <tr><td>Stop location: </td><td>{t_stop_location}</td></tr>
            <tr><td>IP accession: </td><td>{t_ip_accession}</td></tr>
            <tr><td><details><summary>Domain sequence (click to open)</summary>{t_domain_sequence}</details></td></tr>
            '''

        #     domains_dict[everydomain]=[domain_name, domain_order, domain_length, start_location, stop_location, ip_accession]
        #
        # for everydomain in domains_dict.keys():
        #     t_domain_name = domains_dict[everydomain][0]
        #     t_

        single_protein_information += f'''
        </table>
        </details>
        </details>
        '''


    text = f'''
    <html>
        <head>
        <meta charset="UTF-8">
        <title>Cuterle</title>
        <link rel="icon" href="../images/favicon.ico">
        </head>
        <body>
            <img style="max-width:35%;" src="../images/00_logo.png"><br>
            <table style="border:1px solid black">
            <tr>
                <td>Fasta file input:</td>
                <td>{fasta_file}</td>
            </tr>
            <tr>
                <td>TSV file input:</td>
                <td>{tsv_file}</td>
            </tr>
            <tr>
                <td>Number of sequence{plural}:</td>
                <td>{number_of_sequeces}</td>
            </tr>
            <tr>
                <td>Domains found:</td>
                <td>{number_of_domains}</td>
            </tr>
            <table style="border:1px solid black">
                <tr><td>Accession ID</td><td>DOMAIN NAME</td><td>NUMBER OF DOMAINS</td></tr>{one_line_for_every_domain}
            </table>
            {single_protein_information}
        <body>
    </html>
    '''
    return text


def create_html_output(folder_name, fasta_file, tsv_file, result_dictionary, table_list):
    with open(f"{folder_name}/graphical_output.html", "w") as file:
        texts_to_write = html_body(fasta_file, tsv_file, result_dictionary, table_list)
        file.write(texts_to_write)
        # pdfkit.from_file(file)

