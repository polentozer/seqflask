import os
from flask import render_template, url_for, flash, redirect
from seqflask import app
from seqflask.modules import Protein, Nucleotide
from seqflask.forms import nucleotideSequenceForm, proteinSequenceForm, generatorForm
from seqflask.util import random_dna, load_codon_table, fasta_parser

PLOT_DIR = os.path.join(os.path.join(os.getcwd(), f'seqflask/static/images/'))


def dna_operation(list_of_sequences, form):
    CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)

    for target in form.target_organism.choices:
        if target[0] == form.target_organism.data:
            target_organism_name = target[1]

    if form.operation.data == 'translate':
        modified = [single.translate(table=CODON_TABLE, check=True) for single in list_of_sequences]
        if form.plot.data:
            for n, rec in enumerate(list_of_sequences):
                rec.plot_codon_usage(
                    window=16,
                    table=CODON_TABLE,
                    target_organism=target_organism_name,
                    n=n)

    if form.operation.data == 'optimize':
        modified = [single.optimize_codon_usage(table=CODON_TABLE, maximum=form.maximize.data) for single in list_of_sequences]
        if form.golden_gate.data != '0000':
            modified = [single.remove_cutsites(table=CODON_TABLE) for single in modified]
        if form.plot.data:
            for n, rec in enumerate(zip(list_of_sequences, modified)):
                rec[1].plot_codon_usage(
                    window=16,
                    other=rec[0],
                    table=CODON_TABLE,
                    target_organism=target_organism_name,
                    n=n)
        if form.golden_gate.data != '0000':
            modified = [single.make_part(part_type=form.golden_gate.data) for single in modified]

    if form.operation.data == 'harmonize':
        for target in form.source_organism.choices:
            if target[0] == form.source_organism.data:
                source_organism_name = target[1]

        SOURCE_TABLE = load_codon_table(taxonomy_id=form.source_organism.data)

        modified = [single.harmonize(table=CODON_TABLE, source=SOURCE_TABLE, mode=0) for single in list_of_sequences]

        if form.golden_gate.data != '0000':
            modified = [single.remove_cutsites(table=CODON_TABLE) for single in modified]
        if form.plot.data:
            for n, rec in enumerate(zip(list_of_sequences, modified)):
                rec[1].plot_codon_usage(
                    window=16,
                    other=rec[0],
                    other_id=source_organism_name,
                    table=CODON_TABLE,
                    table_other=SOURCE_TABLE,
                    target_organism=target_organism_name,
                    n=n)
        if form.golden_gate.data != '0000':
            modified = [single.make_part(part_type=form.golden_gate.data) for single in modified]

    if form.operation.data =='remove':
        modified = [single.remove_cutsites(table=CODON_TABLE) for single in list_of_sequences]
        if form.plot.data:
            for n, rec in enumerate(list_of_sequences):
                rec.plot_codon_usage(
                    window=16,
                    table=CODON_TABLE,
                    target_organism=target_organism_name,
                    n=n)
        if form.golden_gate.data != '0000':
            modified = [single.make_part(part_type=form.golden_gate.data) for single in modified]
    
    return modified


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/generator", methods=['GET', 'POST'])
def generator():
    form = generatorForm()
    if form.validate_on_submit():
        modified = [Nucleotide(form.sequence_name.data, random_dna(
            form.sequence_length.data,
            homopolymer=form.homopolymer.data,
            gc_stretch=form.max_gc_stretch.data,
            restriction=form.golden_gate.data))]
        return render_template('generator.html', title='GEN-results', modified=modified, form=form)
    return render_template('generator.html', title='Generator', form=form)


@app.route("/dna", methods=['GET', 'POST'])
def dna():
    form = nucleotideSequenceForm()
    for file in os.scandir(PLOT_DIR):
        os.remove(file.path)
    if form.validate_on_submit():
        # job_id  # TODO: make this unique per job and make a db to track settings
        if form.operation.data == 'harmonize' and form.source_organism.data == '0000':
            flash(f'Please select source organism!', 'warning')
            return redirect(url_for('dna', form=form))
        else:
            list_of_sequences = [Nucleotide(rec[0], rec[1]) for rec in fasta_parser(form.dna_sequence.data)]
        
        if not list_of_sequences or len(list_of_sequences[0]) == 0:
            flash(f'Nothing to do here...', 'warning')
            return redirect(url_for('dna', form=form))
        else:
            if form.plot.data:
                for seq in list_of_sequences:
                    if not seq.basic_cds:
                        form.plot.data = False
                        flash("One sequence or more is not a CDS, no plotting for you mister!", "warning")
            modified = dna_operation(list_of_sequences=list_of_sequences, form=form)

        if modified:
            return render_template(
                'dna.html',
                title='DNA',
                form=form,
                modified=modified,
                draw_plot=form.plot.data)

    return render_template('dna.html', title='DNA', form=form)


@app.route("/protein", methods=['GET', 'POST'])
def protein():
    form = proteinSequenceForm()
    for file in os.scandir(PLOT_DIR):
        os.remove(file.path)
    if form.validate_on_submit():
        # job_id  # TODO: make this unique per job and make a db to track settings
        try:
            list_of_sequences = []
            if form.protein_sequence.data:
                list_of_sequences = [Protein(rec[0], rec[1]) for rec in fasta_parser(form.protein_sequence.data)]
            if form.uniprot_identifier.data:
                flash('uniprot', 'success')
            
        except ValueError:
            flash(f'{ValueError}', 'danger')
            return render_template('protein.html', title='Protein', form=form)

        CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)
        
        if form.reverse.data or form.golden_gate.data != '0000':
            modified = [single.reverse_translate(table=CODON_TABLE, maximum=form.maximize.data) for single in list_of_sequences]
            if form.plot.data:
                for target in form.target_organism.choices:
                    if target[0] == form.target_organism.data:
                        target_organism_name = target[1]
                for n, rec in enumerate(modified):
                    rec.plot_codon_usage(
                        window=16,
                        table=CODON_TABLE,
                        target_organism=target_organism_name,
                        n=n)
            if form.golden_gate.data != '0000':
                modified = [single.make_part(part_type=form.golden_gate.data) for single in modified]
        else:
            modified = False

        if not list_of_sequences:
            flash(f'Nothing to do here...', 'warning')
        elif not modified:
            flash(f'Select GoldenGate part or "Reverse-Translate"', 'warning')

        return render_template(
            'protein.html',
            title='PROTEIN',
            form=form,
            modified=modified,
            draw_plot=form.plot.data)

    return render_template('protein.html', title='Protein', form=form)
