from notes_api.database.models.note import Note
from notes_api.database.repositories.base import BaseRepository


class NoteRepository(BaseRepository):
    def __init__(self):
        super().__init__(Note)

    def get_user_notes(self, user_id):
        return Note.query.filter_by(user_id=user_id).all()

    def get_user_note_by_id(self, user_id, note_id):
        return Note.query.filter_by(id=note_id, user_id=user_id).first()
