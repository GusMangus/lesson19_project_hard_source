from marshmallow import Schema, fields

from setup_db import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(nullable=False)
    password = fields.Str(nullable=False)
    role = fields.Str(nullable=False)
