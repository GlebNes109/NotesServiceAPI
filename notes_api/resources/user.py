from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel, ValidationError

from notes_api.database.repositories.user import UserRepository
from notes_api.resources.schemas.schemas import PatchUserSchema

_user_repo = None
def get_user_repo():
    global _user_repo
    if _user_repo is None:
        _user_repo = UserRepository()
    return _user_repo

user_bp = Blueprint('user', __name__)
api = Api(user_bp)

class UserResource(Resource):
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        get_user_repo().delete(user_id)
        return '', 204

    @jwt_required()
    def patch(self):
        json_data = request.get_json()
        try:
            validated = PatchUserSchema(**json_data)
        except ValidationError as e:
            return {"errors": e.errors()}, 400

        user_id = get_jwt_identity()
        user = get_user_repo().get_by_id(user_id)
        fields_to_update = validated.model_dump(exclude_unset=True)
        filtered_fields = {k: v for k, v in fields_to_update.items() if v is not None and v != ''}
        get_user_repo().update(user, **filtered_fields)
        return '', 201

api.add_resource(UserResource, '')
