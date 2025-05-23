import uuid

from notes_api.extensions import db


class Note(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
