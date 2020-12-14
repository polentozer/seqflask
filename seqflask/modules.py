# import logging
import re
import pandas
import matplotlib.pyplot as plt
from flask import url_for
from seqflask.utils import sequence_match, get_codon, GlobalVariables, make_plot_path

plt.switch_backend("Agg")


class Sequence:
    """Biological sequence object"""

    def __init__(self, sequence_id, sequence, logger=None):
        self.sequence_id = sequence_id
        self.sequence = sequence.upper()

    def __repr__(self):
        return f"Sequence: >{self.sequence_id} {self.sequence}"

    def __str__(self):
        return self.sequence

    def __len__(self):
        return len(self.sequence)

    def __eq__(self, other):
        return self.sequence == other.sequence

    @property
    def fasta(self):
        return f">{self.sequence_id}\n\r{self.sequence}\n"

    def kmer_analysis(self, threshold, length=8):
        kmers = {}
        for i in range(len(self) - length + 1):
            kmer = self.sequence[i : i + length]
            if kmer not in kmers:
                kmers[kmer] = 0
            kmers[kmer] += 1

        return [
            a for a in sorted(kmers.items(), key=lambda x: x[1]) if a[1] > threshold
        ][::-1]


class Protein(Sequence):
    """PROTEIN sequence object"""

    def __init__(self, sequence_id, sequence):
        super().__init__(sequence_id, sequence)

    def __add__(self, other):
        return Protein("concat", self.sequence + other.sequence)

    def __repr__(self):
        return f"Protein_Sequence: >{self.sequence_id} {self.sequence}"

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, string):
        allowed_characters = re.compile(r"[^\*\?GALMFWKQESPVICYHRNDTX]")
        if not sequence_match(string, allowed_characters.search):
            raise ValueError(
                f'>{self.sequence_id} :: includes forbidden character(s)! Allowed characters: "GALMFWKQESPVICYHRNDTX?*"'
            )
        self._sequence = string

    def reverse_translate(self, table, maximum=False):
        """Returns optimized DNA sequence"""
        dna_sequence = list()
        if maximum:
            name = "|NUC-MAX"
        else:
            name = "|NUC"
        for amino in self.sequence:
            if amino in "?X":
                dna_sequence.append("NNN")
            else:
                codons = table.loc[amino]
                dna_sequence.append(get_codon(codons, maximum=maximum))

        return Nucleotide(f"{self.sequence_id}{name}", "".join(dna_sequence))


class Nucleotide(Sequence):
    """NUCLEOTIDE sequence object"""

    def __init__(self, sequence_id, sequence, logger=None):
        super().__init__(sequence_id, sequence, logger)

    def __add__(self, other):
        return Nucleotide("concat", self.sequence + other.sequence)

    def __repr__(self):
        return f"Nucleotide_Sequence: >{self.sequence_id} {self.sequence}"

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, string):
        allowed_characters = re.compile(r"[^ACTGNUSW]")
        if not sequence_match(string, allowed_characters.search):
            raise ValueError(
                f'>{self.sequence_id} :: includes forbidden character(s)! Allowed characters: "ACTGN"'
            )
        self._sequence = string

    @property
    def basic_cds(self):
        """Returns True if sequence is CDS or false if its not"""
        if self.sequence[:3] == "ATG" and len(self) % 3 == 0:
            return True
        return False

    def check_cds(self):
        """Checks CDS"""

        def triplet(self):
            return len(self) % 3 == 0

        def start(self):
            return self.sequence[:3] == "ATG"

        def stop(self):
            prot = self.translate(check=True)
            return prot.sequence[-1] == "*"

        def no_internal_stop(self):
            prot = self.translate(check=True)
            return not "*" in prot.sequence[:-1]

        tests = [triplet, start, stop, no_internal_stop]
        result = True
        for test in tests:
            if not test(self):
                result = False

        return result

    @property
    def reverse_complement(self):
        """Returns reverse complement of given DNA sequence"""
        return Nucleotide(
            f"{self.sequence_id}|REVC",
            self.sequence.translate(str.maketrans("ACGT", "TGCA"))[::-1],
        )

    def make_triplets(self):
        """Makes list of chunks 3 characters long from a sequence"""
        return [
            self.sequence[start : start + 3]
            for start in range(0, len(self.sequence), 3)
        ]

    def melting_temperature(self):
        """Calculate and return the Tm using the "Wallace rule".

        Tm = 4°C * (G+C) + 2°C * (A+T)

        The Wallace rule (Thein & Wallace 1986, in Human genetic diseases: a
        practical approach, 33-50) is often used as rule of thumb for approximate
        Tm calculations for primers of 14 to 20 nt length.

        Non-dNA characters (e.g. E, F, J, !, 1, etc) are ignored in this method.
        """
        weak = ("A", "T", "W")
        strong = ("C", "G", "S")
        return 2 * sum(map(self.sequence.count, weak)) + 4 * sum(
            map(self.sequence.count, strong)
        )

    def translate(self, table, check=False):
        """Translate DNA sequence in PROTEIN sequence"""
        # self.logger.debug('Making translation...')
        if not check:
            if not self.basic_cds:
                if "FORCED" not in self.sequence_id:
                    return self
                else:
                    pass
        seq_id = self.sequence_id
        translation = list()
        table = table.reset_index(level="Triplet")
        for triplet in self.make_triplets():
            if len(triplet) == 3 and "N" not in triplet:
                translation.append(table[table["Triplet"] == triplet].index[0])
            else:
                translation.append("?")

        return Protein(f"{seq_id}|PROT", "".join(translation))

    def recode_sequence(self, replace, table, maximum=False):
        """Recode a sequence to replace certain sequences using a given codon table."""
        position = self.sequence.find(replace)
        if position < 0:
            return self
        position -= position % 3
        for i in range(position, position + (len(replace) // 3 + 1) * 3, 3):
            codon = self.sequence[i : i + 3]
            options = table.loc[table.xs(codon, level=1).index[0]]
            if options.shape[0] == 1:
                continue
            if options.shape[0] > 0:
                new_codon = get_codon(
                    options, maximum=maximum, recode=True, skip=[codon]
                )
                break
        if "|REC" not in self.sequence_id:
            self.sequence_id += "|REC"
        self.sequence = f"{self.sequence[:i]}{new_codon}{self.sequence[i+3:]}"

        return self

    def remove_cutsites(self, table, renz=GlobalVariables.RESTRICTION_ENZYMES):
        """Remove recognition sites for restriction enzymes."""
        changes = 0
        for cutsite in renz:
            while cutsite in self.sequence:
                changes += 1
                self = self.recode_sequence(cutsite, table=table)
        print(changes)
        return self

    def optimize_codon_usage(self, table, maximum=False):
        """Optimize codon usage of a given DNA sequence"""
        if not self.basic_cds:
            return self

        seq_id = self.sequence_id
        optimized = self.translate(table=table).reverse_translate(
            table=table, maximum=maximum
        )

        return Nucleotide(f"{seq_id}|OPT", optimized.sequence)

    def make_part(
        self, table, part_type="3t", part_options=GlobalVariables.GGA_PART_TYPES
    ):
        """Make DNA part out of a given sequence"""
        seq_id = f"part_gge{part_type}_{self.sequence_id}"
        part = part_options[part_type]
        if (
            part_type in ("3", "3a", "3b")
            and self.translate(table=table, check=True).sequence[-1] == "*"
        ):
            sequence = f'{part["prefix"]}{self.sequence[:-3]}{part["suffix"]}'
        else:
            sequence = f'{part["prefix"]}{self.sequence}{part["suffix"]}'

        return Nucleotide(seq_id, sequence)

    def harmonize(self, source, table, mode=0):
        """Optimize codon usage of a given DNA sequence
        mode: 0 for closest frequency; 1 for same index"""
        if not self.basic_cds:
            return self

        seq_id = self.sequence_id
        optimized = list()

        for amino, triplet in zip(
            self.translate(table=table).sequence, self.make_triplets()
        ):
            if amino == "?":
                optimized.append("NNN")
            else:
                codons = table.loc[amino]
                source_codons = source.loc[amino]
                sorted_codons_frac = sorted(codons["Fraction"])
                source_codon_frac = source_codons.loc[triplet]["Fraction"]

                if mode == 0:
                    best, freq = 1, 0
                    for cod in sorted_codons_frac:
                        current_best = abs(cod - source_codon_frac)
                        if current_best < best:
                            best, freq = current_best, cod

                    closest_freq_codon = codons[codons["Fraction"] == freq].index[0]
                    optimized.append(closest_freq_codon)

                elif mode == 1:
                    sorted_source_codons = sorted(source_codons["Fraction"])
                    source_codon_index = sorted_source_codons.index(
                        source_codons.loc[amino]["Fraction"]
                    )
                    same_index_codon = codons[
                        codons["Fraction"] == sorted_codons_frac[source_codon_index]
                    ].index[0]
                    optimized.append(same_index_codon)

                else:
                    return self

        return Nucleotide(f"{seq_id}|HARM{mode}", "".join(optimized))

    def plot_codon_usage(
        self,
        table,
        window=16,
        other=None,
        other_id=None,
        table_other=None,
        minmax=True,
        target_organism="Yarrowia lipolytica",
        n=0,
    ):
        """Graph codon frequency of a given gene"""

        def data_fraction(self, table=table, window=window):
            """Calculates average window codon fraction for a given sequence and codon usage table.
            Returns a list of window-fraction values, which can be used for analysis or ploted."""

            values, data = [], []
            codons = table.reset_index().set_index(["Triplet"])

            for triplet in self.make_triplets():
                values.append(codons.loc[triplet]["Fraction"])

            for n in range(len(values) + 1 - window):
                data.append(sum([f for f in values[n : n + window]]) / window)

            return data

        def data_minmax(self, table=table, window=window):
            """Calculates the %MinMax values for a given sequence and codon usage table.
            Returns a list of %MinMax values, which can be used for analysis or ploted.

            Reference:
            Clarke TF IV, Clark PL (2008) Rare Codons Cluster. PLoS ONE 3(10): e3412.
            doi:10.1371/journal.pone.0003412"""

            tri_table = table.reset_index(level="Triplet")
            values, data = [], []

            for triplet in self.make_triplets():
                freq = tri_table[tri_table["Triplet"] == triplet]["Frequency"][0]
                codons = table.loc[tri_table[tri_table["Triplet"] == triplet].index[0]]

                values.append(
                    (
                        freq,
                        max(codons.Frequency),
                        min(codons.Frequency),
                        sum(codons.Frequency) / len(codons),
                    )
                )

            for n in range(len(values) + 1 - window):
                current = values[n : n + window]
                actual = sum([f[0] for f in current]) / window
                maximum = sum([f[1] for f in current]) / window
                minimum = sum([f[2] for f in current]) / window
                average = sum([f[3] for f in current]) / window

                maxi = ((actual - average) / (maximum - average)) * 100
                mini = ((average - actual) / (average - minimum)) * 100

                if maxi > 0:
                    data.append(maxi)
                elif mini > 0:
                    data.append(-mini)

            return data

        if not self.basic_cds:
            return

        if isinstance(other, Nucleotide) and other.basic_cds:
            if minmax:
                data = [
                    x
                    for x in zip(
                        data_minmax(self=self, table=table, window=window),
                        data_minmax(self=other, table=table_other, window=window),
                    )
                ]
            else:
                data = [
                    x
                    for x in zip(
                        data_fraction(self=self, table=table, window=window),
                        data_fraction(self=other, table=table_other, window=window),
                    )
                ]
        else:
            if minmax:
                data = data_minmax(self=self, table=table, window=window)
            else:
                data = data_fraction(self=self, table=table, window=window)

        x = range(len(data))
        zeros = [0 for i in x]

        if other:
            y1 = [i[0] for i in data]
            y2 = [i[1] for i in data]
            _, (ax0, ax1) = plt.subplots(2, 1, sharex=True, figsize=(12, 5))
            plt.subplots_adjust(left=0.08, right=0.98, hspace=0.5)

            ax0.plot(x, y1, alpha=0.8, linewidth=0.5)
            if len(target_organism.split()) > 1:
                ax0.set_title(
                    f"Codon usage plot for {self.sequence_id} in ${target_organism.split()[0]}$ ${target_organism.split()[1]}$"
                )
            else:
                ax0.set_title(
                    f"Codon usage plot for {self.sequence_id} in ${target_organism}$"
                )

            if minmax:
                ax0.set_ylim(-100, 100)
                ax0.axhline(0, color="black", linewidth=0.5)
                ax0.fill_between(
                    x,
                    y1,
                    zeros,
                    where=[True if y > 0 else False for y in y1],
                    alpha=0.5,
                    interpolate=True,
                    color="C0",
                )
                ax0.fill_between(
                    x,
                    y1,
                    zeros,
                    where=[True if y < 0 else False for y in y1],
                    alpha=0.5,
                    interpolate=True,
                    color="C2",
                )
                ax0.set_ylabel("%MinMax Value")
            else:
                ax0.set_ylabel("Fraction")

            if other_id:
                target_organism = other_id

            ax1.plot(x, y2, alpha=0.8, linewidth=0.5)
            if len(target_organism.split()) > 1:
                ax1.set_title(
                    f"Codon usage plot for {other.sequence_id} in ${target_organism.split()[0]}$ ${target_organism.split()[1]}$"
                )
            else:
                ax1.set_title(
                    f"Codon usage plot for {other.sequence_id} in ${target_organism}$"
                )

            if minmax:
                ax1.set_ylim(-100, 100)
                ax1.axhline(0, color="black", linewidth=0.5)
                ax1.fill_between(
                    x,
                    y2,
                    zeros,
                    where=[True if y > 0 else False for y in y2],
                    alpha=0.5,
                    interpolate=True,
                    color="C0",
                )
                ax1.fill_between(
                    x,
                    y2,
                    zeros,
                    where=[True if y < 0 else False for y in y2],
                    alpha=0.5,
                    interpolate=True,
                    color="C2",
                )
                ax1.set_ylabel("%MinMax Value")
            else:
                ax1.set_ylabel("Fraction")

        else:
            _, ax = plt.subplots(1, 1, figsize=(12, 2))
            plt.subplots_adjust(left=0.08, right=0.98, bottom=0.25)
            ax.plot(x, data, alpha=0.8, linewidth=0.5)
            if len(target_organism.split()) > 1:
                ax.set_title(
                    f"Codon usage plot for {self.sequence_id} in ${target_organism.split()[0]}$ ${target_organism.split()[1]}$"
                )
            else:
                ax.set_title(
                    f"Codon usage plot for {self.sequence_id} in ${target_organism}$"
                )

            if minmax:
                ax.set_ylim(-100, 100)
                ax.axhline(0, color="black", linewidth=0.5)
                ax.fill_between(
                    x,
                    data,
                    zeros,
                    where=[True if y > 0 else False for y in data],
                    alpha=0.5,
                    interpolate=True,
                    color="C0",
                )
                ax.fill_between(
                    x,
                    data,
                    zeros,
                    where=[True if y < 0 else False for y in data],
                    alpha=0.5,
                    interpolate=True,
                    color="C2",
                )
                ax.set_ylabel("%MinMax Value")
            else:
                ax.set_ylabel("Fraction")

        plt.xlim(-4, len(data) + 4)
        plt.xlabel("Codon")

        plt.savefig(make_plot_path(n))

        return 0
