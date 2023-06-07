from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import user, password, host, db

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{user}:{password}@{host}/{db}"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

data_category = db.Table('data_category',
                         db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                         db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                         )

data_origin = db.Table('data_origin',
                       db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                       db.Column('origin_id', db.Integer, db.ForeignKey('origin.id'), primary_key=True)
                       )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Danger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    danger_id = db.Column(db.Integer, db.ForeignKey('danger.id'), default=0)

    danger = db.relationship('Danger', backref='data')
    categories = db.relationship('Category', secondary=data_category, backref=db.backref('data', lazy='dynamic'))
    origins = db.relationship('Origin', secondary=data_origin, backref=db.backref('data', lazy='dynamic'))


class Origin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Synonym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)
    name = db.Column(db.String(45), nullable=False)

    data = db.relationship('Data', backref='synonyms')


with app.app_context():
    db.create_all()
    additives_categories = [category[0] for category in db.session.query(Category.name).all()]
