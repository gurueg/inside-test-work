from sqlalchemy import exc
from hashlib import md5
import datetime
import errors

from app import db
from auth import get_auth_token


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModelMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(33))
    token = db.Column(db.String())

    def __init__(self, name, password):
        self.name = name
        self.password = md5(password.encode()).hexdigest()
        self.token = get_auth_token(name)

    @classmethod
    def by_token(cls, token):
        obj = cls.query.filter_by(token=token).first()
        if obj:
            return obj
        else:
            raise errors.AuthError

    @classmethod
    def by_name(cls, name):
        obj = cls.query.filter_by(name=name).first()
        if obj:
            return obj
        else:
            raise errors.AuthError


    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'name': self.name
        }


class Message(db.Model, BaseModelMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, message):
        self.text = message
        self.author = User.by_name(name).id
        self.created_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at,
            'author': User.by_id(self.author).name
        }
