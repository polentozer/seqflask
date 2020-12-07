from random import choice


def random_dna(length, homopolymer=10, gc_stretch=20, max_gc_ratio=0.3, restriction=False):

    dna = ('A', 'C', 'G', 'T')

    restriction_enzymes = [
        "GGTCTC",   # BsaI
        "GAGACC",   # BsaI reverse
        "CGTCTC",   # BsmBI
        "GAGACG",   # BsmBI reverse
        "GCGGCCGC"] # NotI

    SETTINGS = f'''
        length:            {length}
        homopolymer:    -n {homopolymer}
        gc_strech:      -g {gc_stretch}
        restriction:    -e {restriction}
        gc_ratio:       -r {max_gc_ratio}'''


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
        longest, at, gc = 0, 0, 0
        for char in sequence:
            if char in 'GC':
                gc += 1
            elif longest < gc:
                longest = gc
                gc = 0
            if char in 'AT':
                at += 1
            elif longest < at:
                longest = at
                at = 0
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

    candidates, confirmed = [], []
    if length < 100:
        candidates.append(generate(length))
    else:
        while length > 100:
            candidates.append(generate(100))
            length -= 100
        candidates.append(generate(length))

    while candidates:
        if run_tests(candidates[0]):
            candidates.append(generate(len(candidates[0])))
            candidates.pop(0)
        else:
            confirmed.append(candidates[0])
            candidates.pop(0)

    return ''.join(confirmed)
