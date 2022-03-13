<p align="center"><img src="https://github.com/furacca/cuterle/blob/fa5164fc5c15afe030452a95985a0bebce8e6c9e/screenshots/00_logo.png"></p>

# Cuterle
Cuterle is a bioinformatic tool which return an output file (`extracted_domain.fasta`) containing every domain annotated by [InterProScan](https://www.ebi.ac.uk/interpro/) (`~.tsv file`) via Pfam or SMART from the list of protein (`~.fasta file`) submitted.

**Index**
- [Getting started](#getting-started)<br>
- [Usage](#usage)<br>
- [Output example - Fasta list](#output-example---fasta-list)<br>
- [Output example - Sequence's draw](#output-example---sequences-draw)<br>
- [Next updates](#next-updates)<br>

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

### Usage

In terminal, run the following command. By default, this will only retrieve Bulbasaur.

```bash
# Run Cuterle
python3 main.py
```

![](./screenshots/01_first_view.png)


Once you run main.py in terminal, the program request the two input file (~.tsv and ~.fasta).<br>
For every input file there is a check which guarantee its existence and the right format. <br>
**Please be sure to use the right format**

![](./screenshots/02_first_run.png)

## Output example - Fasta list

All the extracted domains have the follow syntax:<br>
- First line: `>{1} - START: {2} - END: {3} - {4} - {5}` 
- Second line: the sequence

Where:
 - {1} - Protein accession (e.g. P51587)
 - {2} - Start location of the domain
 - {3} - End location of the domain
 - {4} - Signature accession (e.g. PF09103 / G3DSA:2.40.50.140)
 - {5} - InterPro annotations - description (e.g. BRCA2 repeat)

At the moment it's possibile to change the syntax only by editing the code. (see: [Next updates](#next-updates))

![](./screenshots/04_first_output.png)


## Output example - Sequence's draw

![](./screenshots/03_first_graphical_output.jpg)

## Next updates

**TOP PRIORITY**
- Enable python argument command line to be bash script friendly (work in progress)

**MEDIUM PRIORITY**
- Use some nice color to draw the domains (same domain, same color)
- Change the way to write down the domains's name (label with the same color of the domain)

**OTHER**
- Possibily of choice for the name's format of sequences in fasta output
- Possibily of choice for the order of domain (decrescent order for number of domain or for the id?)
- Choice the domain of interest to be saved in the output file
- Print max 10 item from the files' list in the folder
- Nicer interface (only at the end)


