#!/usr/bin/env python

from Bio import SeqIO
import argparse
import os

from cigar2aln.cigar import split_cigar_to_tuples
from cigar2aln.alignment import generate_pw_alignment


def one_cigar_to_aln(
        target:SeqIO.SeqRecord, 
        query:SeqIO.SeqRecord, 
        cigar_string:str, 
        output_path:str):
    # Separate cigar string into tuples
    cigar_tuple_list = split_cigar_to_tuples(cigar_string)
    
    target_id = str(target.id)
    target_seq = str(target.seq)
    query_id = str(query.id)
    query_seq = str(query.seq)
    
    # Generate alignment
    target_gapped, query_gapped = generate_pw_alignment(
        target_seq, query_seq, cigar_tuple_list)
    
    # Write alignment to file
    with open(output_path, 'w') as f:
        print(f'>{target_id}', file=f)
        print(target_gapped, file=f)
        print(f'>{query_id}', file=f)
        print(query_gapped, file=f)
        
    return target_gapped, query_gapped, len(target_gapped)

def main(
        target_path:str, 
        query_path:str, 
        paf_path:str, 
        outdir:str='.', 
        format_type:str='fasta'):
    
    # Make output directory if it doesn't exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    get_id = lambda x: x.split(':')[0]
    target_seq_dict = {get_id(rec.id): rec for rec in SeqIO.parse(target_path, format_type)}
    query_seq_dict = {get_id(rec.id): rec for rec in SeqIO.parse(query_path, format_type)}
    with open(paf_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            parts = line.split('\t')
            query_id = parts[0]
            target_id = parts[5]
            
            cigar_string = parts[13].strip('cg:Z:')
            try:
                target_rec = target_seq_dict[target_id]
            except KeyError:
                print(f'Could not find {target_id} entry in target file {target_path}.')
                continue
            try:
                query_rec = query_seq_dict[query_id]
            except KeyError:
                print(f'Could not find {query_id} entry in query file {query_path}.')
                continue
            
            print(f'Processing {query_id} vs {target_id}...')
            
            # Generate alignment
            output_path = f'{outdir.rstrip("/")}/{i:0>4d}_{query_id}_{target_id}.fa'
            target_gapped, query_gapped, gapped_len = one_cigar_to_aln(
                target_rec, query_rec, cigar_string, output_path)
            
            # Write to fasta
            with open(output_path, 'w') as f:
                print(f'>{target_id}', file=f)
                print(target_gapped, file=f)
                print(f'>{query_id}', file=f)
                print(query_gapped, file=f)
                
            print(f'\tWrote {gapped_len} bases to {output_path}.')
            
if __name__ == '__main__':
    # cigar2aln.py
    # Command line program to convert each line in the PAF file into
    # a pairwise alignment in FASTA format.
    #
    # Arguments
    # ---------
    # -t, --target : str
    #   Path to the target FASTA file.
    # -q, --query : str
    #   Path to the query FASTA file.
    # -p, --paf : str
    #   Path to the PAF file.
    # -o, --outdir: str
    #  Path to the output directory.

    parser = argparse.ArgumentParser(description="Convert PAF file to pairwise alignment in FASTA format.")
    parser.add_argument("-t", "--target", type=str, help="Path to the target FASTA file.", required=True)
    parser.add_argument("-q", "--query", type=str, help="Path to the query FASTA file.", required=True)
    parser.add_argument("-p", "--paf", type=str, help="Path to the PAF file.", required=True)
    parser.add_argument("-o", "--outdir", type=str, help="Path to the output directory.", required=True)

    args = parser.parse_args()
    
    main(args.target, args.query, args.paf, args.outdir)
    
    print('Done.')
