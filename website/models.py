from . import db
from flask_login import UserMixin


class Inventory(db.Model):
    __bind_key__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    small = db.Column(db.Integer)
    med = db.Column(db.Integer)
    large = db.Column(db.Integer)
    xl = db.Column(db.Integer)
    xxl = db.Column(db.Integer)
    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    piece = db.relationship('Piece', back_populates='inventory')


class Piece(db.Model):
    __bind_key__ = 'piece'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    prodcost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    inventory = db.relationship('Inventory', back_populates='piece')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(140))
    pieces = db.relationship('Piece')
