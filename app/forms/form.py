from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class RSVP_Form(FlaskForm):
    Pole1 = StringField(label="Gość",validators=[DataRequired()])
    Pole2 = StringField(label="Pole2",validators=[DataRequired()])
    Pole3 = StringField(label="Pole3",validators=[DataRequired()])