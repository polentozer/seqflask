#cSpell: Disable#
COMMON_SPECIES = {
    'ecoli': '83333',
    'yeast':  '4932',
    'human': '9606',
    'bsub': '1432',
    'yali': '284591'}

ORGANISM_CHOICES = [
    ('83333', 'Escherichia coli K12'),
    ('4932', 'Saccharomyces cerevisiae'),
    ('284591', 'Yarrowia lipolytica CLIB122'),
    ('1423', 'Bacilus subtilis'),
    ('1471', 'Bacillus methanolicus'),
    ('9606', 'Homo sapiens'),
    ('1927', 'Streptomyces rimosus')]

DNA_OPERATIONS = [
    ('translate', 'Translate'),
    ('optimize', 'Optimize'),
    ('harmonize', 'Harmonize'),
    ('goldengate', 'Remove GoldenGate cutsites')]

CODONS = [
    'CGA', 'CGC', 'CGG', 'CGT', 'AGA', 'AGG', 'CTA', 'CTC',
    'CTG', 'CTT', 'TTA', 'TTG', 'TCA', 'TCC', 'TCG', 'TCT',
    'AGC', 'AGT', 'ACA', 'ACC', 'ACG', 'ACT', 'CCA', 'CCC',
    'CCG', 'CCT', 'GCA', 'GCC', 'GCG', 'GCT', 'GGA', 'GGC',
    'GGG', 'GGT', 'GTA', 'GTC', 'GTG', 'GTT', 'AAA', 'AAG',
    'AAC', 'AAT', 'CAA', 'CAG', 'CAC', 'CAT', 'GAA', 'GAG',
    'GAC', 'GAT', 'TAC', 'TAT', 'TGC', 'TGT', 'TTC', 'TTT',
    'ATA', 'ATC', 'ATT', 'ATG', 'TGG', 'TAA', 'TAG', 'TGA']

STANDARD_GENETIC_CODE = [
    'R', 'R', 'R', 'R', 'R', 'R', 'L', 'L',
    'L', 'L', 'L', 'L', 'S', 'S', 'S', 'S',
    'S', 'S', 'T', 'T', 'T', 'T', 'P', 'P',
    'P', 'P', 'A', 'A', 'A', 'A', 'G', 'G',
    'G', 'G', 'V', 'V', 'V', 'V', 'K', 'K',
    'N', 'N', 'Q', 'Q', 'H', 'H', 'E', 'E',
    'D', 'D', 'Y', 'Y', 'C', 'C', 'F', 'F',
    'I', 'I', 'I', 'M', 'W', '*', '*', '*']

RENZ_SHORT = [
    'GGTCTC',
    'GAGACC',
    'CGTCTC',
    'GAGACG',
    'GCGGCCGC']

GGA_PART_TYPES = {
    '1': {
        'prefix': 'GCATCGTCTCATCGGAGTCGGTCTCACCCT',
        'suffix': 'AACGAGAGACCAGCAGACCAGAGACGGCAT',
        'info': 'Left side assembly connector'
    },
    '2': {
        'prefix': 'GCATCGTCTCATCGGTCTCAAACG',
        'suffix': 'TATGAGAGACCTGAGACGGCAT',
        'info': 'Promotor'
    },
    '3t': {
        'prefix': 'GCATCGTCTCATCGGTCTCAT',
        'suffix': 'ATCCAGAGACCTGAGACGGCAT',
        'info': 'CDS (with stop)'
    },
    '3a': {
        'prefix': 'GCATCGTCTCATCGGTCTCAT',
        'suffix': 'GGTTCTAGAGACCTGAGACGGCAT',
        'info': 'N-terminal CDS'
    },
    '3b': {
        'prefix': 'GCATCGTCTCATCGGTCTCATTCT',
        'suffix': 'GGATCCAGAGACCTGAGACGGCAT',
        'info': 'CDS'
    },
    '3': {
        'prefix': 'GCATCGTCTCATCGGTCTCAT',
        'suffix': 'GGATCCTGAGACCTGAGACGGCAT',
        'info': 'True type3 CDS (GS linker, no STOP)'
    },
    '4': {
        'prefix': 'GCATCGTCTCATCGGTCTCAATCC',
        'suffix': 'GCTGAGAGACCTGAGACGGCAT',
        'info': 'Terminator'
    },
    '4a': {
        'prefix': 'GCATCGTCTCATCGGTCTCAATCC',
        'suffix': 'TGGCAGAGACCTGAGACGGCAT',
        'info': 'C-terminal CDS'
    },
    '4b': {
        'prefix': 'GCATCGTCTCATCGGTCTCATGGC',
        'suffix': 'GCTGAGAGACCTGAGACGGCAT',
        'info': 'Terminator'
    },
    '5': {
        'prefix': 'GCATCGTCTCATCGGAGTCGGTCTCAGCTG',
        'suffix': 'TACAAGAGACCAGCAGACCAGAGACGGCAT',
        'info': 'Right side assembly connector'
    },
    '6': {
        'prefix': 'GCATCGTCTCATCGGTCTCATACA',
        'suffix': 'GAGTAGAGACCTGAGACGGCAT',
        'info': 'Yeast marker'
    },
    '7': {
        'prefix': 'GCATCGTCTCATCGGTCTCAGAGT',
        'suffix': 'CCGAAGAGACCTGAGACGGCAT',
        'info': "3'-homology or yeast origin"
    },
    '8': {
        'prefix': 'GCATCGTCTCATCGGTCTCACCGA',
        'suffix': 'CCCTAGAGACCAGAGACGGCAT',
        'info': 'E. coli marker and origin'
    },
    '8a': {
        'prefix': 'GCATCGTCTCATCGGTCTCACCGA',
        'suffix': 'CAATAGAGACCAGAGACGGCAT',
        'info': 'E. coli marker and origin'
    },
    '8b': {
        'prefix': 'GCATCGTCTCATCGGTCTCACAAT',
        'suffix': 'CCCTAGAGACCAGAGACGGCAT',
        'info': "5'-homology"
    },
    'X': {
        'prefix': 'GCATCGTCTCATCGGTCTCANNNN',
        'suffix': 'NNNNAGAGACCAGAGACGGCAT',
        'info': 'Custom parts'
    }
}

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(filename)s %(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': 'seqtools.log'
        }
    },
    'loggers': {
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}

