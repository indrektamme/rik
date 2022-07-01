from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, ValidationError
from wtforms.validators import DataRequired, NumberRange
from datetime import date
from flask import flash
from register.models import Company


class RegisterForm(FlaskForm):
    name = StringField('Nimi', validators=[DataRequired()])
    registry_code = IntegerField('Registrikood', validators=[NumberRange(min=1000000, max=9999999)])
    registered = DateField('Registreerimis kuupäev', validators=[DataRequired()])
    submit = SubmitField('Lisa asutajad / omanikud')

    def validate_registered(self, field):
        # Check if not None for that username!
        if field.data > date.today():
            flash('Kuupäev ei tohi olla tulevikus!')
            raise ValidationError("The date cannot be in the future!")

    def validate_name(self, field):
        if Company.query.filter_by(name=field.data).first():
            flash('Selline nimi on juba kasutuses!')
            raise ValidationError('Selline nimi on juba kasutuses!')
        if len(field.data) < 3:
            flash('Nimi peab sisaldama vähemalt 3 tähte!')
            raise ValidationError('Nimi peab sisaldama vähemalt 3 tähte!')
        if len(field.data) > 100:
            flash('Nimi on liiga pikk!')
            raise ValidationError('Nimi on liiga pikk')

    def validate_registry_code(self, field):
        if Company.query.filter_by(registry_code=field.data).first():
            flash('Selline registrikood on juba kasutuses!')
            raise ValidationError('Selline registrikood on juba kasutuses!')


class SearchForm(FlaskForm):
    name = StringField('Nimi')
    registry_code = IntegerField('Registri kood')
    submit = SubmitField('Leia')
