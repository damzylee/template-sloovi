import os
from flask import Flask,jsonify
import json
import datetime
from flask_jwt_extended import JWTManager
from bson.objectid import ObjectId
from dotenv import load_dotenv
from Controllers.template import template_blueprint
from Controllers.user import auth_blueprint

load_dotenv()

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

app.json_encoder = JSONEncoder
app.register_blueprint(template_blueprint)
app.register_blueprint(auth_blueprint)


# Send message incase Authorization Header is missing
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'message': 'Missing Authorization Header'
    }), 401

application = app
   
if __name__ == '__main__':
    app.run(debug=True)