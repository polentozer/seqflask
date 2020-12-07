from flask import render_template, url_for, flash, redirect
from flask_seq import app
from flask_seq.forms import nucleotideSequenceForm, proteinSequenceForm, generatorForm
from flask_seq.generator import random_dna

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/generator", methods=['GET', 'POST'])
def generator():
    form = generatorForm()
    if form.validate_on_submit():
        return render_template('output.html',
                                generated_dna=random_dna(form.sequence_length.data),
                                name=form.sequence_name.data)
    return render_template('generator.html', title='Generator', form=form)


@app.route("/dna", methods=['GET', 'POST'])
def dna():
    form = nucleotideSequenceForm()
    if form.validate_on_submit():
        flash(f'Submitted {form.job_name.data}!', 'success')
        return redirect(url_for('dna'))
    return render_template('dna.html', title='DNA', form=form)


@app.route("/protein", methods=['GET', 'POST'])
def protein():
    form = proteinSequenceForm()
    if form.validate_on_submit():
        flash(f'Submitted {form.job_name.data}!', 'success')
        return redirect(url_for('protein'))
    return render_template('protein.html', title='Protein', form=form)
