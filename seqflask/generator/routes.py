from flask import Blueprint, render_template
from seqflask.generator.forms import generatorForm
from seqflask.generator.utils import random_dna
from seqflask.modules import Nucleotide

generator = Blueprint('generator', __name__)

@generator.route("/generator", methods=['GET', 'POST'])
def generator_page():
    form = generatorForm()
    if form.validate_on_submit():
        modified = [Nucleotide(form.sequence_name.data, random_dna(
            form.sequence_length.data,
            homopolymer=form.homopolymer.data,
            gc_stretch=form.max_gc_stretch.data,
            restriction=form.golden_gate.data))]
        return render_template('generator.html', title='GEN-results', modified=modified, form=form)
    return render_template('generator.html', title='Generator', form=form)

