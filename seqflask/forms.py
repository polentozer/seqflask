import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea
from seqflask.util import load_all_species
from seqflask.seqtools_config import ORGANISM_CHOICES, DNA_OPERATIONS, GGA_PART_TYPES


class nucleotideSequenceForm(FlaskForm):
    dna_sequence = StringField(
        'DNA Sequence(s)',
        widget=TextArea(),
        validators=[DataRequired(), Length(min=10, max=10000)])
    target_organism = SelectField(
        'Select your target organism',
        choices=ORGANISM_CHOICES, default='284591',
        validators=[DataRequired()])
    source_organism = SelectField(
        'Select source organism',
        choices=[('0000', '---')] + ORGANISM_CHOICES,
        default='0000',
        validators=[Optional()])
    operation = RadioField(
        'Select operation',
        choices=DNA_OPERATIONS,
        default='optimize')
    golden_gate = SelectField(
        'Add GoldenGate prefix/sufix for part',
        choices=[('0000', '---')] + [(p, p) for p in GGA_PART_TYPES.keys()],
        default='0000',
        validators=[Optional()])
    maximize = BooleanField(
        'Maximize',
        validators=[Optional()])
    plot = BooleanField(
        'Draw plots',
        validators=[Optional()])
    submit = SubmitField('Submit')


class proteinSequenceForm(FlaskForm):
    uniprot_identifier = StringField(
        'UNIPROT accession number',
        validators=[Optional(), Length(min=6)])
    protein_sequence = StringField(
        'PROTEIN Sequence(s)',
        widget=TextArea(),
        validators=[Optional(), Length(min=1, max=4000)])
    target_organism = SelectField(
        'Select your target organism',
        choices=ORGANISM_CHOICES, default='284591',
        validators=[DataRequired()])
    golden_gate = SelectField(
        'Prepare GoldenGate part',
        choices=[('0000', '---')] + [(p, p) for p in GGA_PART_TYPES.keys() if '3' in p],
        default='0000',
        validators=[Optional()])
    reverse = BooleanField(
        '"Reverse-Translate"',
        validators=[Optional()])
    maximize = BooleanField(
        'Maximize',
        validators=[Optional()])
    plot = BooleanField(
        'Draw plots',
        validators=[Optional()])
    submit = SubmitField('Submit')


class generatorForm(FlaskForm):
    sequence_name = StringField(
        'Sequence name',
        validators=[Optional()])
    sequence_length = IntegerField(
        'Sequence length',
        validators=[DataRequired(), NumberRange(min=1, max=99999)])
    max_gc_stretch = IntegerField(
        'Maximum GC stretch',
        default=20,
        validators=[DataRequired(), NumberRange(min=3)])
    homopolymer = IntegerField(
        'Homopolymer length',
        default=10,
        validators=[DataRequired(), NumberRange(min=1)])
    golden_gate = BooleanField(
        'Remove GoldenGate restriction enzymes',
        validators=[Optional()])
    submit = SubmitField('ORDER NOW!!')
