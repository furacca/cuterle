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
        domain_sorted_list = top_five_domains(result_dictionary, everyprotein)
        t_sequence_len = len(result_dictionary[everyprotein]["Sequence"])

        image = ""
        if t_domains_found > 0:
            image = f'''<img class="preview" src="./preview/prev_{everyprotein}.jpg" alt="Preview of the protein image; if you can read this, then re-run cuterle with -draw_image option">'''
        elif t_domains_found == 0:
            image = '''<p class="preview" align="center"> This protein has no domain to draw. </p>'''

        single_protein_information += f'''
        \n\t\t\t
        <details open>
        <summary class="summary_sequence">
        <b>{everyprotein}</b>
        </summary>
        <table>
            <tbody>
            <tr>
            <td>
                <table>
                <tr>
                    <td style="min-width:400px"> Sequence name: </td>
                    <td>{everyprotein}</td>
                </tr>
                <tr>
                    <td> Length: </td>
                    <td>{t_sequence_len}</td>
                </tr>
                <tr>
                <td> Domains found: </td>
                <td>{t_domains_found}</td></tr>
                <tr>
                    <td><br></td><td><br></td>
                </tr>
                <tr>
                    <td><b> Domain's name </b></td>
                    <td><b>Quantity:</b></td>
                </tr>
{domain_sorted_list}
                </table>
                </td>
                <td>
                {image}
                </td>
            </tr>
            </tbody>
        </table>
        <details>
        <summary class="summary_domain_details">
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

        single_protein_information += f'''
        </table>
        </details>
        <br>
        </details>
        '''


    text = f'''
    <html>
        <head>
        <meta charset="UTF-8">
        <title>Cuterle</title>
        <link rel="icon" href="../images/favicon.ico">
        </head>
        <style>
        
          body {{
          margin: 1%;
          font-family: Arial;
          }}
          
          table, th, td {{
          border: 0px solid black;
          border-collapse: collapse;
          }}
          
          .sub_head {{
          
          }}
          
          .preview {{
          display: block;
          margin-left: auto;
          margin-right: auto;
          width: 50%;
          min-width: 350px;
          }}
          
          .summary_summary {{
          cursor: pointer;
          color: rgb(17, 48, 78);
          background: rgb(219, 226, 239);
          padding: 8px;
          }}
          
          .summary_sequence {{
          cursor: pointer;
          color: rgb(17, 48, 78);
          background: rgb(219, 226, 239);
          padding: 8px;
          }}
          
          .summary_domain_details {{
          cursor: pointer;
          padding: 8px;
          }}
          
          .caption_mod {{
          }}
          
        </style>
        <body>
            <img style="max-width:35%;" src="../images/00_logo.png" alt="CUTERLE'S LOGO"><br>
            
            <details open>
            <br>
            <summary class="summary_summary">
            <b>SUMMARY</b>
            </summary>
            <table>
            <tr>
                <td><b>Fasta file input:</b></td>
                <td>{fasta_file}</td>
            </tr>
            <tr>
                <td><b>TSV file input:</b></td>
                <td>{tsv_file}</td>
            </tr>
            <tr>
                <td><b>Sequence{plural}:</b></td>
                <td>{number_of_sequeces}</td>
            </tr>
            <tr>
                <td><b>Domains found:</td>
                <td>{number_of_domains}</td>
            </tr>
                <tr>
                    <td><br></td><td><br></td>
                    <td><br></td>
                </tr>
                <tr>
                    <td style="min-width:200px"><p class="sub_head"><b>Accession ID</b></p></td>
                    <td style="min-width:500px"><p class="sub_head"><b>DOMAIN NAME</b></p></td>
                    <td><p class="sub_head"><b>NUMBER OF DOMAINS</b></p></td>
                </tr>
{one_line_for_every_domain}
            </table>
            <br>
            </details>
            {single_protein_information}
        </body>
    </html>
    '''
    return text


def create_html_output(folder_name, fasta_file, tsv_file, result_dictionary, table_list):
    with open(f"{folder_name}/graphical_output.html", "w") as file:
        texts_to_write = html_body(fasta_file, tsv_file, result_dictionary, table_list)
        file.write(texts_to_write)

