import pandas as pd

# Sets up spsum format from SPSUM_LABEL ftp://ftp.kazusa.or.jp/pub/codon/current/SPSUM_LABEL
spsum_format = "CGA CGC CGG CGT AGA AGG CTA CTC CTG CTT TTA TTG TCA TCC TCG TCT AGC AGT ACA ACC ACG ACT CCA CCC CCG CCT GCA GCC GCG GCT GGA GGC GGG GGT GTA GTC GTG GTT AAA AAG AAC AAT CAA CAG CAC CAT GAA GAG GAC GAT TAC TAT TGC TGT TTC TTT ATA ATC ATT ATG TGG TAA TAG TGA".split()

table_input = pd.read_excel("/Users/markustadej/Downloads/asd.xlsx",header=0,index_col=1)
tax_ids = [0,1286, 320836, 2908167, 72758, 760530, 562]

table_column = 6

tax_id = tax_ids[table_column]
tax_name = "t_" + table_input.columns[table_column][:table_input.columns[table_column].index("/G")]
codon_frequencies = table_input[table_input.columns[table_column]].to_dict()


def main():
    spsum = [str(codon_frequencies[key]) for key in spsum_format]
    properspsum = " ".join(spsum)

    with open("custom_table.spsum", "a") as custom_table:
        custom_table.write(f"{tax_id}:{tax_name}: {str(sum([codon_frequencies['TAA'], codon_frequencies['TGA'], codon_frequencies['TAG']]))}\n{properspsum}\n")

    print('end')

main()
