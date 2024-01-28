from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,FormField, HiddenField
from wtforms.validators import DataRequired, Length

food_choices = ['Ryba','Mięso','Wege']

class BaseForm(FlaskForm):

    Field1 = StringField(label="Gość",validators=[DataRequired()])
    Field2 = SelectField(label="Czy pojawisz/pojawicie się?",choices=['Tak','Nie'],validators=[DataRequired()])
    Field3 = StringField(label="Email do kontaktu")
    Field4 = StringField(label="Daj/Dajcie proszę znać o ew. wykluczeniach pokarmowych", validators=[Length(max=255)])
    Field9 = StringField(label="Jakiś dodatkowy komentarz?", validators=[Length(max=255)])
    

class AnonymForm(FlaskForm):
    base_form = FormField(BaseForm)
    Field5 = StringField(label="Danie główne czyli dla kogo: Ryba,Mięso lub Wege",validators=[DataRequired(),Length(max=255)])
    form_type = HiddenField()


class OneGuestForm(FlaskForm):
    base_form = FormField(BaseForm)
    Field5 = SelectField(label="Danie główne dla Ciebie",choices=food_choices,validators=[DataRequired()])
    Field6 = SelectField(label="Czy będziesz z osobą towarzyszącą?",choices=['Tak','Nie'],validators=[DataRequired()])
    Field7 = StringField(label="Jeżeli tak, powiedz nam coś o niej. Imię, nazwisko i jakie danie główne sobie życzy.",validators=[Length(max=255)])
    form_type = HiddenField()


class TwoGuestForm(FlaskForm):
    base_form = FormField(BaseForm)
    Field5 = SelectField(label="Danie główne",choices=food_choices,validators=[DataRequired()])
    Field6 = SelectField(label="Danie główne",choices=food_choices,validators=[DataRequired()])
    form_type = HiddenField()


class MultipeGuestForm(FlaskForm):
    base_form = FormField(BaseForm)
    Field5 = SelectField(label="Danie główne",choices=food_choices,validators=[DataRequired()])
    Field6 = SelectField(label="Danie główne",choices=food_choices,validators=[DataRequired()])
    Field7 = SelectField(label="Danie główne",choices=food_choices,validators=[DataRequired()])
    Field8 = SelectField(label="Danie główne",choices=food_choices,validators=[DataRequired()])
    form_type = HiddenField()
