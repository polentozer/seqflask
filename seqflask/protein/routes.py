import os
import time
import requests
from flask import Blueprint, render_template, url_for, flash, redirect
from seqflask.modules import Protein
from seqflask.utils import fasta_parser, load_codon_table, PLOT_DIR
from seqflask.protein.forms import proteinSequenceForm


protein = Blueprint('protein', __name__)


@protein.route("/protein", methods=['GET', 'POST'])
def protein_page():
    form = proteinSequenceForm()
    for file in os.scandir(PLOT_DIR()):
        os.remove(file.path)
    if form.validate_on_submit():
        # job_id  # TODO: make this unique per job and make a db to track settings
        list_of_sequences = []
        if form.protein_sequence.data:
            try:
                list_of_sequences = [Protein(rec[0], rec[1]) for rec in fasta_parser(form.protein_sequence.data)]
            except ValueError as e:
                flash(e, 'danger')
                return render_template('protein.html', title='Protein', form=form)
            except Exception:
                flash('Ups, something went wrong :(', 'danger')
                return redirect(url_for('protein.protein_page'))
        elif form.uniprot_identifier.data:
            uniprot_data = ''
            for uniprot_identifier in str(form.uniprot_identifier.data).split(","):
                uniprot_uri = f"https://www.uniprot.org/uniprot/{uniprot_identifier.replace(' ', '')}.fasta"
                uniprot_response = requests.get(uniprot_uri)
                uniprot_data += (uniprot_response.text)
                time.sleep(0.1)
            try:
                list_of_sequences = [Protein(rec[0], rec[1]) for rec in fasta_parser(uniprot_data)]
                if not list_of_sequences or len(list_of_sequences[0]) == 0:
                    flash(f'404: {form.uniprot_identifier.data} not found!', 'warning')
                    return redirect(url_for('protein.protein_page'))
            except Exception:
                flash('Ups, something went wrong :(', 'danger')
                return redirect(url_for('protein.protein_page'))
                # flash(f'Uniprot {form.uniprot_identifier.data} successfully submitted', 'success')
        else:
            flash(f'Nothing to do here...', 'warning')
            return redirect(url_for('protein.protein_page'))

        CODON_TABLE = load_codon_table(taxonomy_id=form.target_organism.data)
        
        if form.reverse.data or form.golden_gate.data != '0000':
            modified = [single.reverse_translate(table=CODON_TABLE, maximum=form.maximize.data) for single in list_of_sequences]
            if form.golden_gate.data != '0000':
                modified = [single.remove_cutsites(table=CODON_TABLE) for single in modified]
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

        if not list_of_sequences or len(list_of_sequences[0]) == 0:
            flash(f'Nothing to do here...', 'warning')
            return redirect(url_for('protein.protein_page'))
        elif not modified:
            flash(f'Select GoldenGate part or "Reverse-Translate"', 'warning')

        return render_template(
            'protein.html',
            title='PROTEIN',
            form=form,
            modified=modified,
            draw_plot=form.plot.data)

    return render_template('protein.html', title='Protein', form=form)
