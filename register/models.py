from register import db


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    registry_code = db.Column(db.Integer(), unique=True)
    registered = db.Column(db.Date)
    capital = db.Column(db.Integer())

    owns = db.relationship('Ownership', backref='as_legal_person', uselist=False)

    def __init__(self, name, registry_code, registered, capital):
        self.name = name
        self.registry_code = registry_code
        self.registered = registered
        self.capital = capital


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=True, index=True)
    lastname = db.Column(db.String(100), unique=True, index=True)
    personalcode = db.Column(db.Integer(), unique=True)
    owns = db.relationship('Ownership', backref='as_natural_person', uselist=False)

    def __init__(self, firstname, lastname, personalcode):
        self.firstname = firstname
        self.lastname = lastname
        self.personalcode = personalcode


class Ownership(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    owner_as_natural_person = db.Column(db.Integer, db.ForeignKey('persons.id'))
    owner_as_legal_person = db.Column(db.Integer, db.ForeignKey('companies.id'))
    establisher = db.Column(db.Boolean)
    capital = db.Column(db.Integer)

    def __init__(self, company_id, owner_as_natural_person, owner_as_legal_person, establisher, capital):
        self.company_id = company_id
        self.owner_as_natural_person = owner_as_natural_person
        self.owner_as_legal_person = owner_as_legal_person
        self.establisher = establisher
        self.capital = capital
