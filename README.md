<p align="center"><img src="./screenshots/00_logo.png"></p>

# Cuterle
Cuterle is a bioinformatic tool which creates an output file (`extracted_domain.fasta`) containing every domain annotated by [InterProScan](https://www.ebi.ac.uk/interpro/) (`~.tsv file`) via Pfam or SMART analysis from the list of protein (`~.fasta file`) submitted.

This program use two main analysis of InterPro:
- Pfam (XX.X) : A large collection of protein families, each represented by multiple sequence alignments and hidden Markov models (HMMs)
- SMART (X.X) : SMART allows the identification and analysis of domain architectures based on Hidden Markov Models or HMMs

The choice between them are based on which one has more results in ~.tsv file.<br><br>
**Index**
- [Suggested use](#suggested-use)<br>
- [Limitations](#limitations)<br>
- [Getting started](#getting-started)<br>
- [Usage - Manual mode](#usage---manual-mode)<br>
- [Usage - Assisted mode](#usage---assisted-mode)<br>
- [Output example - Fasta list](#output-example---fasta-list)<br>
- [Output example - Sequence's draw](#output-example---sequences-draw)<br>
- [How to get a ~.tsv file](#how-to-get-a-tsv-file)<br>
- [Next updates](#next-updates)<br>
<br>

## Suggested use
This program has been written thinking as **improvement of quality of life** for extracting the domains. <br>
<br>
<i> **Exempli gratia**</i><br>
I want to investigate the relationship between the domains of multiple fishes' species:
1) Download the transcriptome of my species target
2) For each transcriptome obtain a new proteins' fasta list via `hmmsearch` from <a href="http://hmmer.org/">HMMER</a> ---> [species_01_selected_proteins.fasta]
3) Run an InterPro analysis for each sequences in every fasta list
4) Run Cuterle to extract every domain from each sequences choosing an InterPro accession ID for automatic domains' extraction (e.g. IPR002035)
5) Run some MSA and phylogenetic analysis to get some hint about the domain of interest

Thanks to the arguments option, the point 2, 3 and 4 are scriptable, saving **A LOT** of time.<br>





## Limitations
This program does nothing more than extracting the domains from the output of InterPro, 
choosing which method get more results between Pfam and SMART. <br>
It can be helpful when you already have a big protein's list pre-selected by hmmsearch ()



## Getting started

### Prerequisites

- Python3
- pip

### Installation of the Python required packages

Install the required Python packages; while you are in the project's root directory run the following command:

```bash
# Install requirements
pip install -r requirements.txt
```

### Usage - Manual mode
From the release 1.2.0 it's available the **manual mode**, making the program script-friendly.

Asking help to the program:

```
python3 main.py -h
```

```
usage: main.py  [options]

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

optional arguments:
  -h, --help         show this help message and exit
  -m                 Enable the manual mode. -tsv and -fasta argument are requested
  -tsv file.tsv      Input file containing the tsv file output from InterPro
  -fasta file.fasta  Input file containing the fasta sequences
  -a Pfam or SMART   Prior choice between 'Pfam' and 'SMART'. Read the documentation.
  -nf NF             Name format. Read the documentation. Format: [1,2,3,4,5]
  -savetable         Export all kind of domains extracted in ~.csv file, sort by matches
  -draw_image        FOR EACH sequences create a ~.jpg file reporting sequence+domains
```
<br>

Example manual mode syntax:
```
python3 main.py -m -tsv vwf_Homo_sapiens.tsv -fasta vwf_Homo_sapiens.fasta -nf 1,2,3 -savetable -drawimage
```



### Usage - Assisted mode

In terminal run:
```bash
python3 main.py
```
By default, the program will run the assisted mode. <br>
Assisted mode is **a lot** verbose.

<img src="./screenshots/01_first_view.png" width="700">
<!-- ![](./screenshots/01_first_view.png) -->


Once you run main.py in terminal, the program request the two input files (~.tsv and ~.fasta).<br>
For every input file there is a check which guarantee its existence and the right format. <br>
**Please be sure to use the right format**

If you are not sure about how getting the tsv file follow [How to get a ~.tsv file](#how-to-get-a-tsv-file).

Summary table (first column `Domain name`, second column `Domain's number found`) is graphically printed.
It's possible to save it.

<img src="./screenshots/02_first_run.png" width="700">
<br>

## Output example - Fasta list

All the extracted domains have the follow default syntax:<br>
- `>[{1}] - [START: {2}] - [END: {3}] - [{4}] - [{5}]` - First line
- `extracted domain sequence` - Second line

Where every {number} refer to the follow information:
 - {1} - Protein accession (e.g. P51587)
 - {2} - Start location of the domain
 - {3} - End location of the domain
 - {4} - Signature accession (e.g. PF09103 / G3DSA:2.40.50.140)
 - {5} - InterPro annotations - description (e.g. BRCA2 repeat)

At the moment it's possible to change the syntax only by running the manual mode.

<img src="./screenshots/04_extracted_domain_output.png" width="700">

<br><br>

## Output example - Sequence's draw
It's so bad, that's so good. There will be a lot (one or two) updates for the drawing option. See [Next updates](#next-updates).

<img src="./screenshots/03_graphical_output.jpg" width="700">

## How to get a ~.tsv file
There are two main way to get an tsv file from InterPro:
1) Follow the <a href="https://interproscan-docs.readthedocs.io/en/latest/Introduction.html#to-install-and-run-interproscan" target="_blank">InterProScan guide</a> to install and run it on some local machine
2) Use the official <a href="https://www.ebi.ac.uk/interpro/">InterProScan website</a> to submit the fasta fasta file and obtain the tsv file (like in the screenshot below):

2) <img src="./screenshots/06_InterProWebsite.png" width="700">

<br><br>


## Next updates

**TOP PRIORITY**
- None


**MEDIUM PRIORITY**
- Change the InterPro annotation in the draw with the SMART domain description (e.g. from "von Willebrand Factor A" to "VWFA")
- Add a legend for the reduced domain name
- Use some nice color to draw the domains (same domain, same color)
- Change the way to write down the domain's name (label with the same color of the domain)
- Resize the output images without losing too much quality

**LOW PRIORITY**
- None

