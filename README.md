# Cuterle
Bioinformatic tool which extract every domain annotated by InterProScan

![](./screenshots/main_home.png)

## Getting started

### Prerequisites

- Python3
- pip

### Installation

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

## Example of interaction with Cuterle

Once you run main.py in terminal, the program request the two input file (~.tsv and ~.fasta)

![](./screenshots/example_input-output.png)

Output from the inputs above (extracted_domains.fasta)

![](./screenshots/example_output_file.png)


## Next possible feature
Sorted randomly, here we have the next possible feature of Cuterle:

TOP PRIORITY
- Enable python argument command line to be bash script friendly (work in progress)

OTHER

- Nicer interface (only at the end)
- Draw a schematic protein with the domains draw up (potentially done)
- List all the domain extracted in decrescent order (done)
- Possibily of choice for the order of domain (decrescent order for number of domain or for the id?)
- Sort the domain extracted for each sequence in crescent order
- Choice the domain of interest to be saved in the output file
- Print max 10 item from the files' list in the folder

- Maybe a folder "Input/Output" or "Workinprogress" to save every files

