from setuptools import setup, find_packages

setup(
    name='cigar2aln',
    version='0.1.0',
    description='Convert PAF CIGAR strings to pairwise alignments',
    author='Kent Kawashima',
    url='https://github.com/kentwait/cigar2aln',
    author_email='kentkawashima@gmail.com',
    license='Apache 2.0',
    keywords=['bioinformatics', 'mapping', 'alignment', 'cigar', 'fasta', 'paf'],
    packages=find_packages(),
    install_requires=[
        'biopython>=1.78',
    ],
    python_require='>=3.8',
)
