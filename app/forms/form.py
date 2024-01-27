from flask_wtf import FlaskForm
from wtforms import StringField,SelectField
from wtforms.validators import DataRequired


class RSVP_Form(FlaskForm):
    Field1 = StringField(label="Gość",validators=[DataRequired()])
    Field2 = SelectField(label="Czy pojawisz/pojawicie się?",choices=['Tak','Nie'],validators=[DataRequired()])
    Field3 = StringField(label="Daj/Dajcie proszę znać o ew. wykluczeniach pokarmowych")
    Field4 = SelectField(label="Danie główne",choices=['Ryba','Mięso','Wege'],validators=[DataRequired()])