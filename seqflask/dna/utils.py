from seqflask.utils import load_codon_table, GlobalVariables

DNA_OPERATIONS = [
    ("translate", "Translate"),
    ("optimize", "Optimize"),
    ("harmonize", "Harmonize"),
    ("remove", "Remove GoldenGate cutsites"),
]


def dna_operation(list_of_sequences, form):
    CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)

    for target in form.target_organism.choices:
        if target[0] == form.target_organism.data:
            target_organism_name = target[1]

    if form.operation.data == "translate":
        modified = [
            single.translate(table=CODON_TABLE, check=True)
            for single in list_of_sequences
        ]
        if form.plot.data:
            for n, rec in enumerate(list_of_sequences):
                rec.plot_codon_usage(
                    window=GlobalVariables.ANALYSIS_WINDOW,
                    table=CODON_TABLE,
                    target_organism=target_organism_name,
                    n=n,
                )

    if form.operation.data == "optimize":
        if form.set_minimal_optimization.data:
            modified = [
                single.optimize_codon_usage(
                    table=CODON_TABLE,
                    maximum=form.maximize.data
                ).set_minimal_optimization_value(
                    table=CODON_TABLE,
                    threshold=form.minimal_optimization_value.data
                )
                for single in list_of_sequences
            ]
        else:
            modified = [
                single.optimize_codon_usage(table=CODON_TABLE, maximum=form.maximize.data)
                for single in list_of_sequences
            ]
        if form.golden_gate.data != "0000":
            modified = [
                single.remove_cutsites(table=CODON_TABLE) for single in modified
            ]
        if form.plot.data:
            for n, rec in enumerate(zip(list_of_sequences, modified)):
                rec[1].plot_codon_usage(
                    window=GlobalVariables.ANALYSIS_WINDOW,
                    other=rec[0],
                    table=CODON_TABLE,
                    table_other=CODON_TABLE,
                    target_organism=target_organism_name,
                    n=n,
                )
        if form.golden_gate.data != "0000":
            modified = [
                single.make_part(part_type=form.golden_gate.data, table=CODON_TABLE)
                for single in modified
            ]

    if form.operation.data == "harmonize":
        for target in form.source_organism.choices:
            if target[0] == form.source_organism.data:
                source_organism_name = target[1]

        SOURCE_TABLE = load_codon_table(taxonomy_id=form.source_organism.data)

        modified = [
            single.harmonize(table=CODON_TABLE, source=SOURCE_TABLE, mode=0)
            for single in list_of_sequences
        ]
        if form.golden_gate.data != "0000":
            modified = [
                single.remove_cutsites(table=CODON_TABLE) for single in modified
            ]
        if form.plot.data:
            for n, rec in enumerate(zip(list_of_sequences, modified)):
                rec[1].plot_codon_usage(
                    window=GlobalVariables.ANALYSIS_WINDOW,
                    other=rec[0],
                    other_id=source_organism_name,
                    table=CODON_TABLE,
                    table_other=SOURCE_TABLE,
                    target_organism=target_organism_name,
                    n=n,
                )
        if form.golden_gate.data != "0000":
            modified = [
                single.make_part(part_type=form.golden_gate.data, table=CODON_TABLE)
                for single in modified
            ]

    if form.operation.data == "remove":
        modified = [
            single.remove_cutsites(table=CODON_TABLE) for single in list_of_sequences
        ]
        if form.plot.data:
            for n, rec in enumerate(list_of_sequences):
                rec.plot_codon_usage(
                    window=GlobalVariables.ANALYSIS_WINDOW,
                    table=CODON_TABLE,
                    target_organism=target_organism_name,
                    n=n,
                )
        if form.golden_gate.data != "0000":
            modified = [
                single.make_part(part_type=form.golden_gate.data, table=CODON_TABLE)
                for single in modified
            ]

    return modified
