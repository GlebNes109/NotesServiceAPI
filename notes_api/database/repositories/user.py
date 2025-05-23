from notes_api.database.models.user import User
from notes_api.database.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_login(self, login):
        return User.query.filter_by(login=login).first()

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
