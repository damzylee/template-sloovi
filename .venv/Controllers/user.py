from flask import jsonify, request, Blueprint
from flask_jwt_extended import (create_access_token)
from flask_bcrypt import Bcrypt
from Repository.user import UserRepository
from Schemas.schema_user import validate_user
from dotenv import load_dotenv

auth_blueprint = Blueprint('auth_blueprint', __name__)
userRepo = UserRepository()
flask_bcrypt = Bcrypt()
load_dotenv()

# Register route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    ''' register user endpoint '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = userRepo.save(data)
        new_user=userRepo.get_id(new_user)
        new_user['password'] = ''
        response = jsonify(new_user)
        response.status_code = 201
        return response
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

# Login route
@auth_blueprint.route('/login', methods=['POST'])
def auth_user():
    ''' auth endpoint '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = userRepo.get_email(data['email'])
        if flask_bcrypt.check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=data)
            user['token'] = access_token
            return jsonify({'data': user}), 200
        else:
            return jsonify({'message': 'invalid username or password'}), 401
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400