from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from register import db
from register.models import Company, Ownership, Person
from register.companies.forms import RegisterForm, SearchForm
from datetime import datetime, date

companies = Blueprint('companies', __name__)


@companies.route('/', methods=['GET', 'POST'])
def index():

    form = SearchForm()
    result = []
    if form.registry_code.data:
        search_code = "%{}%".format(form.registry_code.data)
        search_name = "%{}%".format(form.name.data)
        result = Company.query.filter(Company.registry_code.like(search_code), Company.name.like(search_name)).all()

    elif form.name.data:
        search_name = "%{}%".format(form.name.data)
        result += Company.query.filter(Company.name.like(search_name)).all()
    else:
        result = Company.query.all()
    return render_template('index.html', form=form, result=result)


@companies.route('/<int:id>/info', methods=['GET', 'POST'])
def info(id):
    company = Company.query.get(id)
    owners = Ownership.query.filter_by(company_id=id)
    owners_list = []
    for o in owners:
        name = ""
        establisher = ""
        if o.establisher:
            establisher = "Asutaja"
        if o.owner_as_natural_person:
            nperson = Person.query.get(o.owner_as_natural_person)
            name = f"{nperson.firstname} {nperson.lastname} (isikukood: {nperson.personalcode})"
        if o.owner_as_legal_person:
            lperson = Company.query.get(o.owner_as_legal_person)
            name = f"{lperson.name} (reg.kood: {lperson.registry_code}"
        owners_list.append({'name': name, 'establisher': establisher, 'capital': o.capital, 'id': o.id})
    return render_template('info.html', company=company, owners=owners_list)


@companies.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        session['name'] = form.name.data
        session['registry_code'] = form.registry_code.data
        session['registered'] = form.registered.data.strftime("%Y-%m-%d")
        session['capital'] = form.capital.data
        return redirect(url_for('owners.add_owners'))

    if "name" in session:
        dat = session['registered'].split("-")
        form.registered.data = datetime(int(dat[0]), int(dat[1]), int(dat[2]))
        form.name.data = session['name']
        form.registry_code.data = session['registry_code']
        form.capital.data = session['capital']
    return render_template('register.html', form=form)
