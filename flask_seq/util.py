import os
from pandas import DataFrame
from random import choice, random
from flask_seq.seqtools_config import COMMON_SPECIES, CODONS, STANDARD_GENETIC_CODE


CODON_USAGE_DB = f'{os.path.dirname(__file__)}/data/codon_usage.spsum'
CUSTOM_CODON_USAGE_DB = f'{os.path.dirname(__file__)}/data/custom_table.spsum'


def fasta_parser(handle):
    '''Parser for fasta sequences.'''
    stream = handle.split('\n')
    sequences = []

    for line in stream:
        if line[0] == '>':
            seq_name = line[1:].strip()
            break
    else:
        return sequences

    temp = []
    for line in stream:
        if line[0] == '>':
            if temp:
                sequences.append((seq_name, "".join(temp)))
            seq_name = line[1:].strip()
            temp = []
            continue
        else:
            temp.append(line.strip().upper())
    else:
        sequences.append((seq_name, "".join(temp)))
    
    # logger.info(f'Input {len(sequences)} sequences...')

    return sequences


def sequence_match(string, search):
    '''Returns TRUE if sequence matches condition in search'''
    # logger.debug('Sequence matching...')
    return not bool(search(string))


def load_all_species(handle=CODON_USAGE_DB):
    lib = []
    with open(handle) as h:
        for header in h:
            h.readline()
            taxid, species = header.strip().split(':')[:2]
            lib.append((taxid, species))
        
        return lib


def load_codon_table(taxonomy_id=None, custom=False, return_name=False):
    '''Load a codon table based on the organism's species ID'''
    # logger.debug(f'load_codon_table(species={species}, taxonomy_id={taxonomy_id}, custom={custom})')
    if custom:
        handle = CUSTOM_CODON_USAGE_DB
    else:
        handle = CODON_USAGE_DB

    with open(handle) as h:
        for header in h:
            codon_counts = h.readline()

            taxid, species = header.strip().split(':')[:2]

            if taxonomy_id:
                taxonomy_id = str(taxonomy_id)

            if taxonomy_id and taxonomy_id != taxid:
                continue

            table = list(
                zip(CODONS, STANDARD_GENETIC_CODE, [int(x) for x in codon_counts.split()]))
            table = DataFrame(table, columns=['Triplet', 'AA', 'Number'])
            table.set_index(['AA', 'Triplet'], inplace=True)
            table.sort_index(inplace=True)
            total = sum(table['Number'])

            table['Fraction'] = table.groupby('AA').transform(lambda x: x / x.sum())
            table['Frequency'] = table['Number'] / total * 1000
            break
    
    if return_name:
        return table, species

    return table


def get_codon(codons, maximum=False, recode=False, skip=[]):
    '''Returns a "locally-optimized" codon. Locally-optimized = mimics the
    codon frequency in the table. Maximum uses the most common codon.'''
    # logger.debug(f'get_codon({list(codons.index)}, maximum={maximum}, recode={recode}, skip={skip})')
    if recode:
        codons = codons.loc[[cod for cod in codons.index if cod not in skip]]
    # Deterministic allocation of codon based on the highest frequency
    if maximum:
        return codons.Fraction.idxmax()
    # Stochastic allocation of codon
    x = codons.Fraction.cumsum() / codons.Fraction.cumsum().max() < random()

    return codons.iloc[x.sum()].name


def codon_table_10plus(table):
    '''Return a codon table only representing codons with > 10% occurrence frequency.'''
    # logger.debug('Generating codon table 10+...')
    table = table[table.Fraction >= 0.1]
    table = table.groupby(level=0).transform(lambda x: x / x.sum())

    return table


def random_dna(length, homopolymer=10, gc_stretch=20, max_gc_ratio=0.3, restriction=False):

    dna = ('A', 'C', 'G', 'T')

    restriction_enzymes = [
        "GGTCTC",   # BsaI
        "GAGACC",   # BsaI reverse
        "CGTCTC",   # BsmBI
        "GAGACG",   # BsmBI reverse
        "GCGGCCGC"] # NotI

    def generate(length, chars=dna):
        return ''.join(choice(chars) for _ in range(length))
    
    def check_restriction(sequence, restriction_set=restriction_enzymes):
        for restriction_site in restriction_set:
            if restriction_site in sequence:
                return True
        return False

    def check_homopolymer(sequence, upper_bound, chars=dna):
        for char in chars:
            if char * upper_bound in sequence:
                return True
        return False

    def check_gc_cont(sequence, lower_bound):
        if not lower_bound < sum(map(sequence.count, ('G', 'C'))) / len(sequence):
            return True
        return False

    def check_gc_stretch(sequence, upper_bound):
        longest, gc = 0, 0
        for char in sequence:
            if char in 'GC':
                gc += 1
            elif longest < gc:
                longest = gc
            if char in 'AT':
                gc = 0
        if longest >= upper_bound:
            return True
        return False

    def run_tests(sequence_string, homopolymer=homopolymer, gc_stretch=gc_stretch,
                  restriction=restriction, max_gc_ratio=max_gc_ratio):
        a = check_homopolymer(sequence_string, upper_bound=homopolymer)
        b = check_gc_stretch(sequence_string, upper_bound=gc_stretch)
        c = False
        d = False
        if restriction:
            c = check_restriction(sequence_string)
        if max_gc_ratio:
            d = check_gc_cont(sequence_string, lower_bound=max_gc_ratio)
        if a or b or c or d:
            return True
        return False


    ## TODO: binary tree search for sequence assembly
    candidates, confirmed = [], []
    treshold = min(gc_stretch, homopolymer) * 5

    if length < treshold:
        candidates.append(generate(length))
    else:
        while length > treshold:
            candidates.append(generate(treshold))
            length -= treshold
        candidates.append(generate(length))

    while candidates:
        if run_tests(candidates[0]):
            l = len(candidates[0])
            candidates.append(generate(l))
            candidates.pop(0)
        else:
            confirmed.append(candidates[0])
            candidates.pop(0)

    return ''.join(confirmed)


DEFAULT_TABLE = load_codon_table(taxonomy_id='284591')
