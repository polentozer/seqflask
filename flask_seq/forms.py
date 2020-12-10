import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea
from flask_seq.seqtools_config import ORGANISM_CHOICES, SOURCE_ORGANISMS, OPERATIONS


class sequenceForm(FlaskForm):
    job_name = StringField('Job name')
    submit = SubmitField('Submit')


class nucleotideSequenceForm(sequenceForm):
    dna_sequence = StringField('DNA Sequence(s)', widget=TextArea(), validators=[
        DataRequired(), Length(min=10, max=10000)])
    target_organism = SelectField('Select your target organism', validators=[DataRequired()],
        choices=ORGANISM_CHOICES, default='284591')
    source_organism = SelectField('Select source organism', validators=[Optional()],
        choices=SOURCE_ORGANISMS, default='0000')
    operation = RadioField('Select operation', choices=OPERATIONS, default='optimize')
    golden_gate = BooleanField('Remove GoldenGate cutsites?', validators=[Optional()])
    maximize = BooleanField('Max?', validators=[Optional()])

    # OPTIONS: manipulate
    # PROPERTIES: target organism (default=yali), source organism (optional)
    # MANIPULATIONS: optimize, harmonize, translate, 
    # EXTRA-FLAGS: maximize, remove-cutsites


class proteinSequenceForm(sequenceForm):
    protein_sequence = StringField('PROTEIN Sequence(s)', validators=[
        DataRequired(), Length(min=1, max=4000)])


class generatorForm(FlaskForm):
    sequence_name = StringField('Sequence name')
    sequence_length = IntegerField('Sequence length', validators=[
        DataRequired(), NumberRange(min=1, max=99999)])
    max_gc_stretch = IntegerField('Maximum GC stretch', default=20, validators=[
        DataRequired(), NumberRange(min=3)])
    homopolymer = IntegerField('Homopolymer length', default=10,
        validators=[DataRequired(), NumberRange(min=3)])
    golden_gate = BooleanField('Remove GoldenGate restriction enzymes?', validators=[Optional()])
    submit = SubmitField('Submit')
