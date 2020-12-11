import os
from flask import render_template, url_for, flash, redirect
from seqflask import app
from seqflask.modules import Protein, Nucleotide
from seqflask.forms import nucleotideSequenceForm, proteinSequenceForm, generatorForm
from seqflask.util import random_dna, load_codon_table, fasta_parser

PLOT_DIR = os.path.join(os.path.join(os.getcwd(), f'seqflask/static/images/'))

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/generator", methods=['GET', 'POST'])
def generator():
    form = generatorForm()
    if form.validate_on_submit():
        seq = random_dna(form.sequence_length.data,
                         homopolymer=form.homopolymer.data,
                         gc_stretch=form.max_gc_stretch.data,
                         restriction=form.golden_gate.data)
        return render_template('generator.html', title='GEN-results', seq=seq, form=form)
    return render_template('generator.html', title='Generator', form=form)


@app.route("/dna", methods=['GET', 'POST'])
def dna():
    form = nucleotideSequenceForm()
    for file in os.scandir(PLOT_DIR):
        os.remove(file.path)
    if form.validate_on_submit():
        # job_id  # TODO: make this unique per job and make a db to track settings
        operation, draw_plot, modified = form.operation.data, None, []
        CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)
        if form.source_organism.data != '0000':
            SOURCE_TABLE = load_codon_table(taxonomy_id=form.source_organism.data)

        input_sequences = [Nucleotide(rec[0], rec[1]) for rec in fasta_parser(form.dna_sequence.data)]
        
        for target in form.target_organism.choices:
            if target[0] == form.target_organism.data:
                target_organism_name = target[1]

        if operation == 'translate':
            modified = [single.translate(table=CODON_TABLE, check=True) for single in input_sequences]

        if operation == 'optimize':
            modified = [single.optimize_codon_usage(table=CODON_TABLE, maximum=form.maximize.data) for single in input_sequences]
            if form.golden_gate.data:
                modified = [single.remove_cutsites(table=CODON_TABLE) for single in modified]
            if form.plot.data:
                draw_plot = True
                for n, rec in enumerate(zip(input_sequences, modified)):
                    rec[1].plot_codon_usage(
                        window=16,
                        other=rec[0],
                        table=CODON_TABLE,
                        target_organism=target_organism_name,
                        n=n)

        if operation == 'harmonize':
            if form.source_organism.data == '0000':
                flash(f'Please select source organism!', 'warning')
                
            else:
                for target in form.source_organism.choices:
                    if target[0] == form.source_organism.data:
                        source_organism_name = target[1]
                modified = [single.harmonize(table=CODON_TABLE, source=SOURCE_TABLE, mode=0) for single in input_sequences]
                if form.golden_gate.data:
                    modified = [single.remove_cutsites(table=CODON_TABLE) for single in modified]
                if form.plot.data:
                    draw_plot = True
                    for n, rec in enumerate(zip(input_sequences, modified)):
                        rec[1].plot_codon_usage(
                            window=16,
                            other=rec[0],
                            other_id=source_organism_name,
                            table=CODON_TABLE,
                            table_other=SOURCE_TABLE,
                            target_organism=target_organism_name,
                            n=n)

        if operation =='goldengate' and form.golden_gate.data == '0':
            modified = [single.remove_cutsites(table=CODON_TABLE) for single in input_sequences]

        if form.golden_gate.data != '0':
            modified = [single.make_part(part_type=form.golden_gate.data) for single in modified]


        if modified:
            flash(f'Submitted!', 'success')
            return render_template(
                'dna.html',
                title='DNA',
                form=form,
                modified=modified,
                draw_plot=draw_plot,
                seq_num=len(modified))

    return render_template('dna.html', title='DNA', form=form)


@app.route("/protein", methods=['GET', 'POST'])
def protein():
    form = proteinSequenceForm()
    if form.validate_on_submit():
        # job_id  # TODO: make this unique per job and make a db to track settings
        CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)
        input_sequences = [Protein(rec[0], rec[1]) for rec in fasta_parser(form.protein_sequence.data)]

        print(form.golden_gate.data)
        if form.golden_gate.data != '0':
            modified = [single.reverse_translate(table=CODON_TABLE, maximum=form.maximize.data).make_part(part_type=form.golden_gate.data) for single in input_sequences]
        elif form.reverse.data:
            modified = [single.reverse_translate(table=CODON_TABLE, maximum=form.maximize.data) for single in input_sequences]
        else:
            modified = False

        if not modified:
            flash(f'Select GoldenGate part or "Reverse-Translate"', 'warning')
        else:
            flash(f'Submitted!', 'success')
        return render_template('protein.html', title='PROTEIN', form=form, modified=modified)

    return render_template('protein.html', title='Protein', form=form)
