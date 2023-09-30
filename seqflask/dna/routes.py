import os
from flask import Blueprint, render_template, url_for, flash, redirect, current_app
from seqflask.modules import Nucleotide
from seqflask.utils import fasta_parser, GlobalVariables, clean_old_plots, clean_old_fasta
from seqflask.dna.forms import nucleotideSequenceForm
from seqflask.dna.utils import dna_operation


dna = Blueprint("dna", __name__)


@dna.route("/dna", methods=["GET", "POST"])
def dna_page():
    form = nucleotideSequenceForm()
    clean_old_plots()
    clean_old_fasta()
    if form.validate_on_submit():
        if form.operation.data == "harmonize" and form.source_organism.data == "0000":
            flash(f"Please select source organism!", "warning")
            return render_template("dna.html", title="DNA", form=form)

        try:
            list_of_sequences = [
                Nucleotide(rec[0], rec[1])
                for rec in fasta_parser(form.dna_sequence.data)
            ]
        except ValueError as e:
            flash(e, "danger")
            return render_template("dna.html", title="DNA", form=form)
        except Exception:
            flash("Ups, something went wrong :(", "danger")
            return redirect(url_for("dna.dna_page"))

        if not list_of_sequences or len(list_of_sequences[0]) == 0:
            flash(f"Nothing to do here...", "warning")
            return redirect(url_for("dna.dna_page"))
        else:
            if form.plot.data:
                for seq in list_of_sequences:
                    if not seq.basic_cds:
                        form.plot.data = False
                        flash(
                            "One sequence or more is not a CDS. No plotting for you!",
                            "warning",
                        )
            modified = dna_operation(list_of_sequences=list_of_sequences, form=form)

        if modified:
            with open(f"{os.path.join(current_app.root_path,f'static/temp/data.fasta')}", "w") as fasta_file_output:
                for single in modified:
                    fasta_file_output.write(single.fasta)
            return render_template(
                "dna.html",
                title="DNA",
                form=form,
                modified=modified,
                draw_plot=form.plot.data,
            )

    return render_template("dna.html", title="DNA", form=form)
