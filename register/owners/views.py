from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from register import db
from register.models import Ownership, Person, Company
from register.owners.forms import OwnershipForm
from datetime import datetime, date

owners = Blueprint('owners', __name__)


def natural_person_choices():
    choices = [(0, '')]
    choices1 = Person.query.all()

    for element in choices1:
        sequence = (element.id, element.firstname + ' ' + element.lastname + ' ' + str(element.personalcode))
        choices.append(sequence)
    return choices


def legal_person_choices():
    choices = [(0, '')]
    choices1 = Company.query.all()
    for element in choices1:
        sequence = (element.id, element.name)
        choices.append(sequence)
    return choices


@owners.route('/owners', methods=['GET', 'POST'])
def add_owners():
    form = OwnershipForm()
    if form.submit.data:
        if form.capital_share.data and (form.owner_as_natural_person.data or form.owner_as_legal_person.data):
            owner = {
                     'owner_as_natural_person': form.owner_as_natural_person.data,
                     'owner_as_natural_person_name': get_person_name(form.owner_as_natural_person.data),
                     'owner_as_legal_person': form.owner_as_legal_person.data,
                     'owner_as_legal_person_name': get_company_name(form.owner_as_legal_person.data),
                     'capital_share': form.capital_share.data
                     }
            if 'owners' in session and session['owners']:
                add_owner_to_session(owner)
            else:
                session['owners'] = [owner]

            return redirect(url_for('owners.add_owners'))
    form.owner_as_natural_person.choices = natural_person_choices()
    form.owner_as_legal_person.choices = legal_person_choices()
    return render_template('add_owner.html', form=form)


@owners.route('/save', methods=['GET', 'POST'])
def save():
    if validate_owners_data():
        try:
            company = Company(name=session['name'], registry_code=session['registry_code'], registered=string_to_date(session['registered']), capital=session['capital'])
            db.session.add(company)
            db.session.commit()

            k = session['owners']
            for owner in k:
                ownership = Ownership(company_id=company.id,
                                      owner_as_natural_person=owner['owner_as_natural_person'],
                                      owner_as_legal_person=owner['owner_as_legal_person'],
                                      establisher=True,
                                      capital=owner['capital_share'])
                db.session.add(ownership)
                db.session.commit()

            flash('Ettevõte on edukalt salvestatud!')
            session.clear()
            return redirect(url_for('companies.info', id=company.id))
        except Exception as e:
            print(e)

    return redirect(url_for('owners.add_owners'))


def validate_owners_data():
    if 'owners' in session and session['owners']:
        k = session['owners']
        if len(k) < 1:
            flash("ettevõttel peab olema vähemalt üks omanik")
            return False
        capital_sum = 0
        for owner in k:
            capital_sum += int(owner['capital_share'])
        if capital_sum != session['capital']:
            flash(f"Liikmete kapitali summa {capital_sum} € on erinev ettevõtte põhikapitalist {session['capital']} €.")
            return False
        return True
    else:
        flash("ettevõttel peab olema vähemalt üks omanik")
        return False


def get_company_name(id):
    if id:
        return Company.query.get(id).name
    return ''


def get_person_name(id):
    if id:
        return Person.query.get(id).firstname + " " + Person.query.get(id).lastname
    return None


def add_owner_to_session(new_owner):
    k = session['owners']
    for idx, owner in enumerate(k):
        if new_owner['owner_as_natural_person']:
            if new_owner['owner_as_natural_person'] == owner['owner_as_natural_person']:
                k[idx] = new_owner
                session['owners'] = k
                return
                break
        if new_owner['owner_as_legal_person']:
            if new_owner['owner_as_legal_person'] == owner['owner_as_legal_person']:
                k[idx] = new_owner
                session['owners'] = k
                return
    k.append(new_owner)
    session['owners'] = k


@owners.route('/delete_owners_from_session', methods=['GET', 'POST'])
def delete_owners_from_session():
    if 'owners' in session and session['owners']:
        session.pop('owners')
    return redirect(url_for('owners.add_owners'))


def string_to_date(date_str):
    dat = date_str.split("-")
    return datetime(int(dat[0]), int(dat[1]), int(dat[2]))
