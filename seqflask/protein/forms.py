from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from seqflask.utils import GlobalVariables


class proteinSequenceForm(FlaskForm):
    uniprot_identifier = StringField(
        "UNIPROT accession number", validators=[Optional(), Length(min=6)]
    )
    protein_sequence = StringField(
        "PROTEIN Sequence(s)",
        widget=TextArea(),
        validators=[Optional(), Length(min=1, max=40000)],
    )
    target_organism = SelectField(
        "Select your target organism",
        choices=GlobalVariables.ORGANISM_CHOICES,
        default="284591",
        validators=[DataRequired()],
    )
    golden_gate = SelectField(
        "Prepare GoldenGate part",
        choices=[("0000", "---")]
        + [
            (k, v["info"])
            for k, v in GlobalVariables.GGA_PART_TYPES.items()
            if "3" in k
        ],
        default="0000",
        validators=[Optional()],
    )
    minimal_optimization_value = IntegerField(
        "Input minimal optimization value",
        default=0,
        validators=[Optional(), NumberRange(min=-50, max=50)],
    )
    reverse = BooleanField("To DNA", validators=[Optional()])
    maximize = BooleanField("Maximize", validators=[Optional()])
    plot = BooleanField("Draw plots", validators=[Optional()])
    set_minimal_optimization = BooleanField("Set optimization value", validators=[Optional()])
    submit = SubmitField("Submit")
