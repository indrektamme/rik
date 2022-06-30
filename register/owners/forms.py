from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class OwnershipForm(FlaskForm):
    choices = []
    company_id = IntegerField('Company')
    owner_as_natural_person = SelectField('Omanik (füüsiline isik)', coerce=int, choices=choices, validators=[NumberRange(min=1)])
    owner_as_legal_person = SelectField('Omanik (juriidiline isik)', coerce=int, choices=choices, validators=[NumberRange(min=1)])
    establisher = BooleanField('Establisher')
    capital_share = IntegerField('Põhikapital (€): ')
    submit = SubmitField('Lisa osanik')
