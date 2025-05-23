from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from notes_api.extensions import db


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def create(self, **kwargs):
        try:
            obj = self.model(**kwargs)
            db.session.add(obj)
            print(db.session)
            print("Session bind:", db.session.get_bind())
            print("App:", current_app)
            db.session.commit()
            return obj
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def update(self, obj, **kwargs):
        try:
            for attr, value in kwargs.items():
                setattr(obj, attr, value)
            db.session.commit()
            return obj
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def delete(self, obj):
        try:
            db.session.delete(obj)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
