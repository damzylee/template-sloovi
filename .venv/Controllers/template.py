from flask import jsonify, request, Blueprint
from flask_jwt_extended import (jwt_required)
from Repository.template import TemplateRepository
from Schemas.schema_template import validate_template
from dotenv import load_dotenv

template_blueprint = Blueprint('template_blueprint', __name__)
templateRepo = TemplateRepository()
load_dotenv()

# Get all template route
@template_blueprint.route('/template', methods=['GET'])
@jwt_required()
def get_templates():
    templates = templateRepo.get_all()
    response = jsonify(templates)
    response.status_code = 200
    return response

# Post template
@template_blueprint.route('/template', methods=['POST'])
@jwt_required()
def save_template():
    data = validate_template(request.get_json())
    if data['ok']:
        template = request.get_json()
        new_template = templateRepo.save(template)
        response = jsonify(templateRepo.get_id(new_template))
        response.status_code = 201
        return response
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

# get one template by id
@template_blueprint.route('/template/<string:template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    template = templateRepo.get_id(template_id)
    response = jsonify(template)
    response.status_code = 200
    return response

# Update template
@template_blueprint.route('/template/<string:template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    body = request.get_json()
    body["_id"] = template_id
    updated = templateRepo.update(body)
    if updated >= 1:
        response = jsonify(templateRepo.get_id(template_id))
        response.status_code = 200
        return response
    else:
        response = jsonify({"status_code": 404})
    return response

# Delete template
@template_blueprint.route('/template/<string:template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    deleted = templateRepo.delete(template_id)
    if deleted >= 1:
        response = jsonify({"status_code": 200})
    else:
        response = jsonify({"status_code": 404})
    return response