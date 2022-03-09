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
