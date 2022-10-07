# cSpell: disable
import os
from random import random
from pandas import DataFrame
from flask import current_app


class GlobalVariables:
    CODONS = [
        "CGA",
        "CGC",
        "CGG",
        "CGT",
        "AGA",
        "AGG",
        "CTA",
        "CTC",
        "CTG",
        "CTT",
        "TTA",
        "TTG",
        "TCA",
        "TCC",
        "TCG",
        "TCT",
        "AGC",
        "AGT",
        "ACA",
        "ACC",
        "ACG",
        "ACT",
        "CCA",
        "CCC",
        "CCG",
        "CCT",
        "GCA",
        "GCC",
        "GCG",
        "GCT",
        "GGA",
        "GGC",
        "GGG",
        "GGT",
        "GTA",
        "GTC",
        "GTG",
        "GTT",
        "AAA",
        "AAG",
        "AAC",
        "AAT",
        "CAA",
        "CAG",
        "CAC",
        "CAT",
        "GAA",
        "GAG",
        "GAC",
        "GAT",
        "TAC",
        "TAT",
        "TGC",
        "TGT",
        "TTC",
        "TTT",
        "ATA",
        "ATC",
        "ATT",
        "ATG",
        "TGG",
        "TAA",
        "TAG",
        "TGA",
    ]
    STANDARD_GENETIC_CODE = [
        "R",
        "R",
        "R",
        "R",
        "R",
        "R",
        "L",
        "L",
        "L",
        "L",
        "L",
        "L",
        "S",
        "S",
        "S",
        "S",
        "S",
        "S",
        "T",
        "T",
        "T",
        "T",
        "P",
        "P",
        "P",
        "P",
        "A",
        "A",
        "A",
        "A",
        "G",
        "G",
        "G",
        "G",
        "V",
        "V",
        "V",
        "V",
        "K",
        "K",
        "N",
        "N",
        "Q",
        "Q",
        "H",
        "H",
        "E",
        "E",
        "D",
        "D",
        "Y",
        "Y",
        "C",
        "C",
        "F",
        "F",
        "I",
        "I",
        "I",
        "M",
        "W",
        "*",
        "*",
        "*",
    ]
    ORGANISM_CHOICES = [
        ("56364", "Agrotis ipsilon: (10)"),
        ("180454", "*Anopheles gambiae str. PEST (13330)"),
        ("3702", "Arabidopsis thaliana (82082)"),
        ("5580", "Aureobasidium pullulans (13)"),
        ("1471", "Bacillus methanolicus (21)"),
        ("1423", "Bacillus subtilis (2529)"),
        ("302911", "Bifidobacterium animalis subsp. lactis (29)"),
        ("224326", "Borrelia burgdorferi B31 (1639)"),
        ("9913", "Bos taurus (13374)"),
        ("5476", "Candida albicans (1148)"),
        ("3483", "Cannabis sativa: (8)"),
        ("13429", "Cinnamomum camphora: (5)"),
        ("431943", "Clostridium kluyveri DSM 555 (3913)"),
        ("243230", "Deinococcus radiodurans R1 (3106)"),
        ("121845", "*Diaphorina citri: (22814)"),
        ("37762", "Escherichia coli (8089)"),
        ("44745", "Haematococcus pluvialis (CAUTION: FROM 23 GENES ONLY!!)"),
        ("9606", "Homo sapiens (93487)"),
        ("284590", "Kluyveromyces lactis NRRL Y-1140 (5217)"),
        ("1589", "Lactobacillus pentosus (6)"),
        ("203120", "Leuconostoc mesenteroides subsp. mesenteroides ATCC 8293 (2005)"),
        ("13632", "*Lucilia sericata: (23715)"),
        ("1163748", "*Marinobacter hydrocarbonoclasticus (H. nauticus) (3610)"),
        ("265072", "Methylobacillus flagellatus KT (2753)"),
        ("29057", "Ostrinia nubilalis: (57)"),
        ("553", "Pantoea ananatis (9)"),
        ("5076", "Penicillium chrysogenum (164)"),
        ("160488", "Pseudomonas putida (6891)"),
        ("4932", "Saccharomyces cerevisiae (14411)"),
        ("4932.mitochondrion", "Saccharomyces cerevisiae mitochondrion (89)"),
        ("4896", "Schizosaccharomyces pombe (6109)"),
        ("246200", "Silicibacter pomeroyi (4252)"),
        ("7107", "Spodoptera exigua: (38)"),
        ("1927", "Streptomyces rimosus (29)"),
        ("431241", "Trichoderma reesei QM6a (8439)"),
        ("7111", "*Trichoplusia ni: (23623)"),
        ("5421", "Xanthophyllomyces dendrorhous (34)"),
        ("284591", "Yarrowia lipolytica CLIB122 (5967)"),
        ("263930", "Yponomeuta evonymellus: (222)"),
        ("4577", "*Zea mays: (57651)"),
        ("82528", "Crocus sativus (26)"),
        ("28540", "Buddleja davidii (5)"),
        ("1148", "Synechoscystis sp. PCC6803 (3623)"),
    ]
    RESTRICTION_ENZYMES = [
        "GGTCTC",   # BsaI
        "GAGACC",   # BsaI reverse
        "CGTCTC",   # BsmBI
        "GAGACG",   # BsmBI reverse
        "GCGGCCGC", # NotI
    ]
    GGA_PART_TYPES = {
        "1": {
            "prefix": "GCATCGTCTCATCGGAGTCGGTCTCACCCT",
            "suffix": "AACGAGAGACCAGCAGACCAGAGACGGCAT",
            "info": "Type1: Left side assembly connector",
        },
        "2": {
            "prefix": "GCATCGTCTCATCGGTCTCAAACG",
            "suffix": "TATGAGAGACCTGAGACGGCAT",
            "info": "Type2: Promotor",
        },
        "3t": {
            "prefix": "GCATCGTCTCATCGGTCTCAT",
            "suffix": "ATCCAGAGACCTGAGACGGCAT",
            "info": "Type3t: CDS (with stop)",
        },
        "3a": {
            "prefix": "GCATCGTCTCATCGGTCTCAT",
            "suffix": "GGTTCTAGAGACCTGAGACGGCAT",
            "info": "Type3a: N-terminal CDS",
        },
        "3b": {
            "prefix": "GCATCGTCTCATCGGTCTCATTCT",
            "suffix": "GGATCCAGAGACCTGAGACGGCAT",
            "info": "Type3b: CDS",
        },
        "3": {
            "prefix": "GCATCGTCTCATCGGTCTCAT",
            "suffix": "GGATCCTGAGACCTGAGACGGCAT",
            "info": "Type3: True YTK type3 CDS (GS linker, no STOP)",
        },
        "4": {
            "prefix": "GCATCGTCTCATCGGTCTCAATCC",
            "suffix": "GCTGAGAGACCTGAGACGGCAT",
            "info": "Type4: Terminator",
        },
        "4a": {
            "prefix": "GCATCGTCTCATCGGTCTCAATCC",
            "suffix": "TGGCAGAGACCTGAGACGGCAT",
            "info": "Type4a: C-terminal CDS",
        },
        "4b": {
            "prefix": "GCATCGTCTCATCGGTCTCATGGC",
            "suffix": "GCTGAGAGACCTGAGACGGCAT",
            "info": "Type4b: Terminator",
        },
        "5": {
            "prefix": "GCATCGTCTCATCGGAGTCGGTCTCAGCTG",
            "suffix": "TACAAGAGACCAGCAGACCAGAGACGGCAT",
            "info": "Type5: Right side assembly connector",
        },
        "6": {
            "prefix": "GCATCGTCTCATCGGTCTCATACA",
            "suffix": "GAGTAGAGACCTGAGACGGCAT",
            "info": "Type6: Yeast marker",
        },
        "7": {
            "prefix": "GCATCGTCTCATCGGTCTCAGAGT",
            "suffix": "CCGAAGAGACCTGAGACGGCAT",
            "info": "Type7: 3'-homology or yeast origin",
        },
        "8": {
            "prefix": "GCATCGTCTCATCGGTCTCACCGA",
            "suffix": "CCCTAGAGACCAGAGACGGCAT",
            "info": "Type8: E. coli marker and origin",
        },
        "8a": {
            "prefix": "GCATCGTCTCATCGGTCTCACCGA",
            "suffix": "CAATAGAGACCAGAGACGGCAT",
            "info": "Type8a: E. coli marker and origin",
        },
        "8b": {
            "prefix": "GCATCGTCTCATCGGTCTCACAAT",
            "suffix": "CCCTAGAGACCAGAGACGGCAT",
            "info": "Type8b: 5'-homology",
        },
        "X": {
            "prefix": "GCATCGTCTCATCGGTCTCANNNN",
            "suffix": "NNNNAGAGACCAGAGACGGCAT",
            "info": "TypeX: Custom parts",
        },
    }


def clean_old_plots():
    for file in os.scandir(os.path.join(current_app.root_path, "static/images/")):
        if file.name[-4:] == ".png":
            os.remove(file.path)


def make_plot_path(n):
    return f"{os.path.join(current_app.root_path, f'static/images/plot{n+1}.png')}"


def fasta_parser(handle):
    """Parser for fasta sequences."""
    stream = handle.split("\n")
    sequences = []

    for line in stream:
        if line.strip()[0] == ">":
            seq_name = line.strip()[1:71]
            break
    else:
        return sequences

    temp = []
    for line in stream:
        if line and line.strip()[0] == ">":
            if temp:
                sequences.append((seq_name, "".join(temp)))
            seq_name = line.strip()[1:71]
            temp = []
            continue
        else:
            temp.append(line.strip().upper())
    else:
        sequences.append((seq_name, "".join(temp)))

    return sequences


def sequence_match(string, search):
    """Returns TRUE if sequence matches condition in search"""
    return not bool(search(string))


def load_codon_table(taxonomy_id=None, custom=False, return_name=False):
    """Load a codon table based on the organism's species ID"""
    if custom:
        handle = os.path.join(current_app.root_path, "data/custom_table.spsum")
    else:
        handle = os.path.join(current_app.root_path, "data/codon_usage.spsum")

    with open(handle) as h:
        for header in h:
            codon_counts = h.readline()

            taxid, species = header.strip().split(":")[:2]

            if taxonomy_id:
                taxonomy_id = str(taxonomy_id)

            if taxonomy_id and taxonomy_id != taxid:
                continue

            table = list(
                zip(
                    GlobalVariables.CODONS,
                    GlobalVariables.STANDARD_GENETIC_CODE,
                    [int(x) for x in codon_counts.split()],
                )
            )
            table = DataFrame(table, columns=["Triplet", "AA", "Number"])
            table.set_index(["AA", "Triplet"], inplace=True)
            table.sort_index(inplace=True)
            total = sum(table["Number"])

            table["Fraction"] = table.groupby("AA").transform(lambda x: x / x.sum())
            table["Frequency"] = table["Number"] / total * 1000
            break

    if return_name:
        return table, species

    return table


def get_codon(codons, maximum=False, recode=False, skip=[]):
    """Returns a "locally-optimized" codon. Locally-optimized = mimics the
    codon frequency in the table. Maximum uses the most common codon."""
    if recode:
        codons = codons.loc[[cod for cod in codons.index if cod not in skip]]
    # Deterministic allocation of codon based on the highest frequency
    if maximum:
        return codons.Fraction.idxmax()
    # Stochastic allocation of codon
    x = codons.Fraction.cumsum() / codons.Fraction.cumsum().max() < random()

    return codons.iloc[x.sum()].name
