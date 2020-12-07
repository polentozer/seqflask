import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class sequenceForm(FlaskForm):
    job_name = StringField('Job name')
    submit = SubmitField('Submit')


class nucleotideSequenceForm(sequenceForm):
    dna_sequence = StringField('DNA Sequence(s)', validators=[
        DataRequired(), Length(min=10, max=10000)])
    harmonize = BooleanField('Harmonize')


class proteinSequenceForm(sequenceForm):
    protein_sequence = StringField('PROTEIN Sequence(s)', validators=[
        DataRequired(), Length(min=1, max=4000)])


class generatorForm(FlaskForm):
    sequence_name = StringField('Sequence name')
    sequence_length = IntegerField('Sequence length', validators=[
        DataRequired(), NumberRange(min=1, max=10000)])
    protein = BooleanField('Protein?')
    submit = SubmitField('Submit')
