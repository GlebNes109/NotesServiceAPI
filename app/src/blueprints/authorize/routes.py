from flask_restful import Resource, Api

from app.src.blueprints.authorize import auth_bp

api = Api(auth_bp)

class Auth(Resource):
    def get(self, todo_id):
        return {todo_id: [todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(Auth, '/<string:todo_id>')