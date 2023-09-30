from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, RadioField, IntegerField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from seqflask.utils import GlobalVariables
from seqflask.dna.utils import DNA_OPERATIONS


class nucleotideSequenceForm(FlaskForm):
    dna_sequence = StringField(
        "DNA Sequence(s)",
        widget=TextArea(),
        validators=[DataRequired(), Length(min=10, max=10000)],
    )
    target_organism = SelectField(
        "Select your target organism",
        choices=GlobalVariables.ORGANISM_CHOICES,
        default="284591",
        validators=[DataRequired()],
    )
    source_organism = SelectField(
        "Select source organism",
        choices=[("0000", "---")] + GlobalVariables.ORGANISM_CHOICES,
        default="0000",
        validators=[Optional()],
    )
    operation = RadioField(
        "Select operation", choices=DNA_OPERATIONS, default="optimize"
    )
    golden_gate = SelectField(
        "Add GoldenGate prefix/suffix for part",
        choices=[("0000", "---")]
        + [(k, v["info"]) for k, v in GlobalVariables.GGA_PART_TYPES.items()],
        default="0000",
        validators=[Optional()],
    )
    minimal_optimization_value = IntegerField(
        "Input minimal optimization value",
        default=0,
        validators=[Optional(), NumberRange(min=-50, max=50)],
    )
    maximize = BooleanField("Maximize", validators=[Optional()])
    plot = BooleanField("Draw plots", validators=[Optional()])
    set_minimal_optimization = BooleanField("Optimization value", validators=[Optional()])
    submit = SubmitField("Submit")
