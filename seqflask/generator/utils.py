from random import choice
from seqflask.utils import GlobalVariables

def random_dna(length, homopolymer=10, gc_stretch=20, max_gc_ratio=0.3, restriction=False):

    dna = ('A', 'C', 'G', 'T')

    def generate(length, chars=dna):
        return ''.join(choice(chars) for _ in range(length))
    
    def check_restriction(sequence, restriction_set=GlobalVariables.RESTRICTION_ENZYMES):
        for restriction_site in restriction_set:
            if restriction_site in sequence:
                return True
        return False

    def check_homopolymer(sequence, upper_bound, chars=dna):
        for char in chars:
            if char * (upper_bound+1) in sequence:
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

