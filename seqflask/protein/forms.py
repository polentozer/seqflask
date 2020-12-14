from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Optional
from seqflask.utils import GlobalVariables


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
        choices=GlobalVariables.ORGANISM_CHOICES, default='284591',
        validators=[DataRequired()])
    golden_gate = SelectField(
        'Prepare GoldenGate part',
        choices=[('0000', '---')] + [(k, v['info']) for k, v in GlobalVariables.GGA_PART_TYPES.items() if '3' in k],
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
