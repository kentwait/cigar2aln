# cigar2aln

Converts CIGAR string of tartget and query sequences into a pairwise alignment


## Required packages

- biopython>=1.78

## Installation

```
pip install git+https://github.com/kentwait/cigar2aln.git
```

## Usage

```
> from cigar2aln.cigar import split_cigar_to_tuples
> from cigar2aln.alignment import generate_pw_alignment

> cigar_string = "5=3X2=1D4I"
> cigar_tuples = split_cigar_to_tuples(cigar_string)
> cigar_tuples
[(5, '='), (3, 'X'), (2, '='), (1, 'D'), (4, 'I')]

> target_sequence = "ATCGCTAGGAT"
> query_sequence = "ATCGCCTAGAAAAA"
> generate_pw_alignment(target_sequence, query_sequence, cigar_tuples)
("ATCGCTAGGAT----", "ATCGCCTAGA-AAAA")

```

## Command-line interface

Prepare the following files

- Tab-delimited .paf file  
The PAF file must have at least 13 columns. The 13th column should contain the CIGAR string representating the mapping between the target reference sequence and the query sequence
- Target FASTA-formatted file  
Entry IDs need to match the target ID in column 6 of the PAF file. If the target ID is not found in the target file, the corresponding alignment in the PAF file is skipped.
- Query FASTA-formatted file  
Entry IDs need to match the target ID in column 1 of the PAF file. If the query ID is not found in the query file, the corresponding alignment in the PAF file is skipped.

The full set of arguments to run the command-line program `cigar2aln.py` are listed below.
```
$ python cigar2aln.py -h

usage: cigar2aln.py [-h] -t TARGET -q QUERY -p PAF -o OUTDIR

Convert PAF file to pairwise alignment in FASTA format.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Path to the target FASTA file.
  -q QUERY, --query QUERY
                        Path to the query FASTA file.
  -p PAF, --paf PAF     Path to the PAF file.
  -o OUTDIR, --outdir OUTDIR
                        Path to the output directory.
```
