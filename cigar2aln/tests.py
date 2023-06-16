import unittest

from cigar2aln.cigar import split_cigar_to_tuples, generate_cigar_from_pwaln
from cigar2aln.alignment import generate_pw_alignment

class TestAlignmentFunctions(unittest.TestCase):

    def test_separate_cigar(self):
        cigar_string = "5=3X2=1D4I"
        expected_output = [(5, '='), (3, 'X'), (2, '='), (1, 'D'), (4, 'I')]
        self.assertEqual(split_cigar_to_tuples(cigar_string), expected_output)

    def test_generate_alignment(self):
        cigar_tuples = [(5, '='), (3, 'X'), (2, '='), (1, 'D'), (4, 'I')]
        target_sequence = "ATCGCTAGGAT"
        query_sequence = "ATCGCCTAGAAAAA"
        expected_output = [
            "ATCGCTAGGAT----",
            "ATCGCCTAGA-AAAA"
        ]
        self.assertEqual(
            generate_pw_alignment(target_sequence, query_sequence, cigar_tuples), 
            expected_output)

    def test_generate_cigar(self):
        alignment = [
            "ATCGCTAGGAT----",
            "ATCGCCTAGA-AAAA"
        ]
        expected_output = "5=3X2=1D4I"
        self.assertEqual(
            generate_cigar_from_pwaln(*alignment), 
            expected_output)
