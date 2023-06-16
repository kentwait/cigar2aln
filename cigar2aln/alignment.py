from typing import List, Tuple


def generate_pw_alignment(
        target_sequence:str, 
        query_sequence:str, 
        cigar_tuples:List[Tuple[int, str]]) -> Tuple[str, str]:
    # Initialize empty alignment for target and query sequences
    target_gapped_sequence = ''
    query_gapped_sequence = ''

    t_pos = 0  # Current position in the target sequence
    q_pos = 0  # Current position in the query sequence

    for count, symbol in cigar_tuples:
        if symbol == 'M':
            # Does not differentiate between identical (=) and mismatch (X)
            target_gapped_sequence += target_sequence[t_pos : t_pos + count]
            query_gapped_sequence += query_sequence[q_pos : q_pos + count]
            t_pos += count
            q_pos += count
        if symbol == '=':
            target_gapped_sequence += target_sequence[t_pos : t_pos + count]
            query_gapped_sequence += query_sequence[q_pos : q_pos + count]
            t_pos += count
            q_pos += count
        elif symbol == 'X':
            target_gapped_sequence += target_sequence[t_pos : t_pos + count]
            query_gapped_sequence += query_sequence[q_pos : q_pos + count]
            t_pos += count
            q_pos += count
        elif symbol == 'D':
            target_gapped_sequence += target_sequence[t_pos : t_pos + count]
            query_gapped_sequence += '-' * count
            t_pos += count
        elif symbol == 'I':
            target_gapped_sequence += '-' * count
            query_gapped_sequence += query_sequence[q_pos : q_pos + count]
            q_pos += count

    return target_gapped_sequence, query_gapped_sequence
