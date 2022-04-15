from Bio import SeqIO


def result_dictionary_maker(protein_list, dataframe_tsv, prior_choice, fasta_file, domain_order):
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
