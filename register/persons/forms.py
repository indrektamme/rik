from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class PersonForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    personalcode = IntegerField('Personal code', validators=[NumberRange(min=30000000000, max=69999999999)])
    submit = SubmitField('Salvesta')
