#!/usr/bin/python3

import sys
import argparse

gencode_11 = {
"TTT":"F","TCT":"S","TAT":"Y","TGT":"C",
"TTC":"F","TCC":"S","TAC":"Y","TGC":"C",
"TTA":"L","TCA":"S","TAA":"-","TGA":"-",
"TTG":"L","TCG":"S","TAG":"-","TGG":"W",
"CTT":"L","CCT":"P","CAT":"H","CGT":"R",
"CTC":"L","CCC":"P","CAC":"H","CGC":"R",
"CTA":"L","CCA":"P","CAA":"Q","CGA":"R",
"CTG":"L","CCG":"P","CAG":"Q","CGG":"R",
"ATT":"I","ACT":"T","AAT":"N","AGT":"S",
"ATC":"I","ACC":"T","AAC":"N","AGC":"S",
"ATA":"I","ACA":"T","AAA":"K","AGA":"R",
"ATG":"M","ACG":"T","AAG":"K","AGG":"R",
"GTT":"V","GCT":"A","GAT":"D","GGT":"G",
"GTC":"V","GCC":"A","GAC":"D","GGC":"G",
"GTA":"V","GCA":"A","GAA":"E","GGA":"G",
"GTG":"V","GCG":"A","GAG":"E","GGG":"G"}

# Sets up spsum format from SPSUM_LABEL ftp://ftp.kazusa.or.jp/pub/codon/current/SPSUM_LABEL
spsum_format = "CGA CGC CGG CGT AGA AGG CTA CTC CTG CTT TTA TTG TCA TCC TCG TCT AGC AGT ACA ACC ACG ACT CCA CCC CCG CCT GCA GCC GCG GCT GGA GGC GGG GGT GTA GTC GTG GTT AAA AAG AAC AAT CAA CAG CAC CAT GAA GAG GAC GAT TAC TAT TGC TGT TTC TTT ATA ATC ATT ATG TGG TAA TAG TGA".split()


def parse_options():
    """
    python spsum_from_cds.py <path-to-fasta-with-genes.fasta> -i <taxid> -n <organism name>
    """
    parser = argparse.ArgumentParser(description='Generate a frequency file from a CDS fasta file used for the codonharmonizer')

    parser.add_argument(dest="fasta_filepath", help="DNA multi-fasta file of protein coding genes", metavar="CDS-FASTA")
    parser.add_argument("-n, --name", dest="tax_name", required=True, help="Name of the organism", metavar="NAME")
    parser.add_argument("-i, --id", dest="taxid", required=True, help="NCBI TaxID of the organism", metavar="TAXID")
    parser.add_argument("-q, --quiet", dest="quiet", action='store_true', help="Ignore warnings")

    inputs = parser.parse_args()

    return inputs


def get_sequences(fasta_contents):
    """Given a fasta file, return a dictionary of the entries"""
    try:
        sequence_dic = {}
        header = ""
        for line in fasta_contents:
            if line[0] == '>':
                header = line.strip()[1:]
                sequence_dic[header] = ""
            else:
                clean_seq = line.strip().upper().replace("U", "T")

                if header == "":
                    raise ValueError()

                sequence_dic[header] += clean_seq

        return sequence_dic

    except ValueError as err:
        sys.stderr.write("Not a valid DNA fasta file (missing header)")
        sys.exit()


def split_to_codons(sequence, header, quiet):
    """Returns a codon list from a sequence reading frame +1 """
    valid_bases = "ATCG"
    codon_sequence_list = []
    if len(sequence) % 3 == 0:
        codon_sequence_list = [sequence[i:i+3] for i in range(0,len(sequence),3)]
    elif not quiet:
            print("NOT USED: Partial sequence >"+header+" not divisible by complete codons")

    codon_sequence_list_clean = []
    for codon in codon_sequence_list:
        if all(char in valid_bases for char in codon):
            codon_sequence_list_clean.append(codon)
        elif not quiet:
            print("Removed codon sequence",codon,"containing non DNA letter from:", header)
    return codon_sequence_list_clean


# def main():
def main(argv):
    inputs = parse_options()
    
    # fasta_filepath = '/Users/markustadej/Projects/seqflask/seqflask/data/GCF_015586225.1_ASM1558622v1_cds_from_genomic.fna'
    # taxid = '1234'
    # tax_name = 'Test testis sub. test'
    # quiet = True

    try:
        with open(inputs.fasta_filepath, "r") as fasta_input:
        # with open(fasta_filepath, "r") as fasta_input:
            fastafile = fasta_input.readlines()
    except (OSError, IOError) as err:
        print("Unable to open input fasta file")
        sys.exit()

    fasta = get_sequences(fastafile)
    number_of_genes = len(fasta)
    if number_of_genes < 100:
        print("WARNING: Number of genes < 100")


    codon_frequencies = {}
    for entry in fasta:
        # codons = split_to_codons(fasta[entry], entry, quiet)
        codons = split_to_codons(fasta[entry], entry, inputs.quiet)
        for codon in codons:
            if codon not in codon_frequencies.keys():
                codon_frequencies[codon] = 1
            else:
                codon_frequencies[codon] += 1

    
    spsum = [str(codon_frequencies[key]) for key in spsum_format]
    properspsum = " ".join(spsum)

    with open("custom_table.spsum", "a") as custom_table:
        custom_table.write(f"{inputs.taxid}:{inputs.tax_name}: {str(sum([codon_frequencies['TAA'], codon_frequencies['TGA'], codon_frequencies['TAG']]))}\n{properspsum}\n")
        # custom_table.write(f"{taxid}:{tax_name}: {str(sum([codon_frequencies['TAA'], codon_frequencies['TGA'], codon_frequencies['TAG']]))}\n{properspsum}")

    # print(f"{taxid}:{tax_name}: {str(sum([codon_frequencies['TAA'], codon_frequencies['TGA'], codon_frequencies['TAG']]))}\n{properspsum}")
    # test_id = '13632'

    # with open("codon_usage.spsum", 'r') as handle:
    #     codon_usage_spsum_table = handle.readlines()

    # for i, line in enumerate(codon_usage_spsum_table):
    #     if i%2 == 0 or i == 0:
    #         temporary_data = line.strip().split(":")
    #         taxid = temporary_data[0]
    #         species_name = ' '.join(temporary_data[1:-1])
    #         gene_number = temporary_data[-1]

    #         # print(taxid, species_name, gene_number)
    #     if test_id == taxid:
    #         print(i, 'here')
    #         break    

    print('end')



if __name__ == "__main__":
    main(sys.argv[1:])
    # main()
