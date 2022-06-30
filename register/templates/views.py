from flask import render_template, url_for, flash, redirect, request, Blueprint
from register import db
from register.models import Person
from register.persons.forms import PersonForm

persons = Blueprint('persons', __name__)


@persons.route('/persons', methods=['GET', 'POST'])
def list():
    persons_list = Person.query.all()
    form = PersonForm()
    if form.validate_on_submit():
        person = Person(firstname=form.firstname.data, lastname=form.lastname.data, personalcode=form.personalcode.data)
        db.session.add(person)
        db.session.commit()
        return redirect(url_for('persons.list'))
    return render_template('persons.html', form=form, persons_list=persons_list)
