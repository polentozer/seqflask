import os
from flask import Blueprint, render_template, url_for, flash, redirect
from seqflask.modules import Nucleotide
from seqflask.utils import fasta_parser, GlobalVariables, clean_old_plots
from seqflask.dna.forms import nucleotideSequenceForm
from seqflask.dna.utils import dna_operation


dna = Blueprint('dna', __name__)


@dna.route("/dna", methods=['GET', 'POS.T'])
def dna_page():
    form = nucleotideSequenceForm()
    clean_old_plots()
    if form.validate_on_submit():
        # job_id  # TODO: make this unique per job and make a db to track settings
        if form.operation.data == 'harmonize' and form.source_organism.data == '0000':
            flash(f'Please select source organism!', 'warning')
            return render_template('dna.html', title='DNA', form=form)

        try:
            list_of_sequences = [Nucleotide(rec[0], rec[1]) for rec in fasta_parser(form.dna_sequence.data)]
        except ValueError as e:
            flash(e, 'danger')
            return render_template('dna.html', title='DNA', form=form)
        except Exception:
            flash('Ups, something went wrong :(', 'danger')
            return redirect(url_for('dna.dna_page'))
        
        if not list_of_sequences or len(list_of_sequences[0]) == 0:
            flash(f'Nothing to do here...', 'warning')
            return redirect(url_for('dna.dna_page'))
        else:
            if form.plot.data:
                for seq in list_of_sequences:
                    if not seq.basic_cds:
                        form.plot.data = False
                        flash("One sequence or more is not a CDS. No plotting for you mister!", "warning")
            modified = dna_operation(list_of_sequences=list_of_sequences, form=form)

        if modified:
            return render_template(
                'dna.html',
                title='DNA',
                form=form,
                modified=modified,
                draw_plot=form.plot.data)

    return render_template('dna.html', title='DNA', form=form)

