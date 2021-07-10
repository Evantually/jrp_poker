from app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    chips = db.Column(db.Integer)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suit = db.Column(db.String(64))
    face_value = db.Column(db.String(64))
    img_path = db.Column(db.String(128))
    value = db.Column(db.Integer)