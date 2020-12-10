from flask import render_template, url_for, flash, redirect
from flask_seq import app
from flask_seq.util import random_dna, load_codon_table
from flask_seq.fasta_io import fasta_parser
from flask_seq.modules import Protein, Nucleotide
from flask_seq.forms import nucleotideSequenceForm, proteinSequenceForm, generatorForm

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
    if form.validate_on_submit():
        # print(form.target_organism.data)
        JOB_ID = form.job_name.data  # TODO: make this unique per job and make db to track settings
        CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)
        if form.source_organism.data != '0000':
            SOURCE_TABLE = load_codon_table(taxonomy_id=form.source_organism.data)

        input_sequences = [Nucleotide(rec[0], rec[1]) for rec in fasta_parser(form.dna_sequence.data)]

        if form.operation.data == 'translate':
            modified = [single.translate(table=CODON_TABLE, check=True) for single in input_sequences]
        if form.operation.data == 'optimize':
            modified = [single.optimize_codon_usage(table=CODON_TABLE, maximum=form.maximize.data) for single in input_sequences]
        if form.operation.data == 'harmonize':
            modified = [single.harmonize(table=CODON_TABLE, source=SOURCE_TABLE, mode=0) for single in input_sequences]
        if form.operation.data =='goldengate':
            modified = [single.remove_cutsites(table=CODON_TABLE) for single in input_sequences]
        if form.golden_gate.data and form.operation.data != 'translate':
            modified = [single.remove_cutsites(table=CODON_TABLE) for single in modified]



        flash(f'Submitted {form.job_name.data}!', 'success')
        # return redirect(url_for('dna'))
        return render_template('dna.html', title='DNA', form=form, modified=modified)
    return render_template('dna.html', title='DNA', form=form)


@app.route("/protein", methods=['GET', 'POST'])
def protein():
    form = proteinSequenceForm()
    if form.validate_on_submit():
        flash(f'Submitted {form.job_name.data}!', 'success')
        return redirect(url_for('protein'))
    return render_template('protein.html', title='Protein', form=form)
