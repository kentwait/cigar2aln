from typing import List, Tuple
import re


CIGAR_PATTERN = r'(\d+)([A-Za-z=]+)'
cigar_re = re.compile(CIGAR_PATTERN)

def split_cigar_to_tuples(cigar_string:str) -> List[Tuple[int, str]]:
    matches = cigar_re.findall(cigar_string)
    cigar_tuples = [(int(count), symbol) for count, symbol in matches]
    return cigar_tuples

def generate_cigar_from_pwaln(target_sequence:str, query_sequence:str) -> str:
    cigar_string = ""
    count = 0
    prev_symbol = ""

    for t, q in zip(target_sequence, query_sequence):
        if t == '-' and q != '-':
            symbol = 'I'
        elif t != '-' and q == '-':
            symbol = 'D'
        elif t != '-' and q != '-' and t == q:
            symbol = '='
        else:
            symbol = 'X'

        if symbol == prev_symbol:
            count += 1
        else:
            if prev_symbol:
                cigar_string += str(count) + prev_symbol
            count = 1
            prev_symbol = symbol

    # Add the last symbol and count
    cigar_string += str(count) + prev_symbol

    return cigar_string

def test_cigar(
        target_gapped_sequence:str, 
        query_gapped_sequence:str, 
        expected_cigar_string:str) -> bool:
    # Check if cigar string is the same
    cigar_string = generate_cigar_from_pwaln(target_gapped_sequence, query_gapped_sequence)
    return expected_cigar_string == cigar_string
