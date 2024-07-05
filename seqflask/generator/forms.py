from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional


class generatorForm(FlaskForm):
    sequence_name = StringField("Sequence name", validators=[Optional()])
    sequence_length = IntegerField(
        "Sequence length", validators=[DataRequired(), NumberRange(min=1, max=99999)]
    )
    gc_percent = IntegerField(
        "GC percent",
        default=35,
        validators=[DataRequired(), NumberRange(min=0, max=100)],
    )
    max_gc_stretch = IntegerField(
        "Max GC stretch",
        default=20,
        validators=[DataRequired(), NumberRange(min=3)],
    )
    homopolymer = IntegerField(
        "Homopolymer",
        default=10,
        validators=[DataRequired(), NumberRange(min=1)],
    )
    golden_gate = BooleanField(
        "Remove GoldenGate restriction enzymes", validators=[Optional()]
    )
    submit = SubmitField("ORDER NOW!!")
