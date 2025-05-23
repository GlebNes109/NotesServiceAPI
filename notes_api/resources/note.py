from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel, ValidationError

from notes_api.database.repositories.notes import NoteRepository

_note_repo = None
def get_note_repo():
    global _note_repo
    if _note_repo is None:
        _note_repo = NoteRepository()
    return _note_repo

note_bp = Blueprint('note', __name__)
api = Api(note_bp)

class NoteSchema(BaseModel):
    title: str | None = None
    text: str | None = None

class Notes(Resource):
    @jwt_required()
    def post(self):
        json_data = request.get_json()
        try:
            validated = NoteSchema(**json_data)
        except ValidationError as e:
            return {"errors": e.errors()}, 400

        user_id = get_jwt_identity()
        note = get_note_repo().create(user_id=user_id, title=validated.title, text=validated.text)
        return {"note_id": note.id}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        notes = get_note_repo().get_user_notes(user_id)
        return [{"id": n.id, "title": n.title, "text": n.text} for n in notes], 200

class NoteResource(Resource):
    @jwt_required()
    def get(self, note_id):
        user_id = get_jwt_identity()
        note = get_note_repo().get_by_id(note_id)
        if not note:
            return {}, 404
        if note.user_id != user_id:
            return {}, 403
        return {"id": note.id, "title": note.title, "text": note.text}, 200

    @jwt_required()
    def patch(self, note_id):
        json_data = request.get_json()
        try:
            validated = NoteSchema(**json_data)
        except ValidationError as e:
            return {"errors": e.errors()}, 400

        note = get_note_repo().get_by_id(note_id)
        if not note:
            return {}, 404
        user_id = get_jwt_identity()
        if note.user_id != user_id:
            return {}, 403
        note = get_note_repo().get_by_id(note_id)
        fields_to_update = validated.model_dump(exclude_unset=True)
        filtered_fields = {k: v for k, v in fields_to_update.items() if v is not None and v != ''}
        updated_note = get_note_repo().update(note, **filtered_fields)
        return {"note_id": updated_note.id}, 200

    @jwt_required()
    def delete(self, note_id):
        note = get_note_repo().get_by_id(note_id)
        if not note:
            return {}, 404
        user_id = get_jwt_identity()
        if note.user_id != user_id:
            return {}, 403

        get_note_repo().delete(note_id)
        return '', 204

api.add_resource(Notes, '')
api.add_resource(NoteResource, '/<note_id>')
