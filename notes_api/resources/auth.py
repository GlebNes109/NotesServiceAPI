from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from notes_api.database.repositories.user import UserRepository
from notes_api.resources.schemas.schemas import SignupSchema, SigninSchema

# user_repo = UserRepository()

_user_repo = None

def get_user_repo():
    global _user_repo
    if _user_repo is None:
        _user_repo = UserRepository()
    return _user_repo

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

class SignupResource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            validated = SignupSchema(**json_data)
        except ValidationError as e:
            return {"errors": e.errors()}, 400

        hashed_password = generate_password_hash(validated.password)
        # user_repo = UserRepository()
        try:
            user = get_user_repo().create(
                login=validated.login,
                email=validated.email,
                password=hashed_password
            )
        except IntegrityError:
            return {"error": "такой пользователь уже есть"}, 409
        token = create_access_token(identity=user.id)
        return {'token': token, 'user_id': user.id}, 201

class SigninResource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            validated = SigninSchema(**json_data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 400
        user_repo = UserRepository()
        user = user_repo.get_by_login(validated.login)
        if user and check_password_hash(user.password, validated.password):
            token = create_access_token(identity=user.id)
            return {'token': token, 'user_id': user.id}, 200
        return {'message': 'Invalid credentials'}, 409


api.add_resource(SignupResource, '/signup')
api.add_resource(SigninResource, '/signin')
