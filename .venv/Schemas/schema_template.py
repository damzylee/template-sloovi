from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

template_schema = {
    "type": "object",
    "properties": {
        "template_name": {
            "type": "string",
        },
        "subject": {
            "type": "string",
        },
        "body": {
            "type": "string"
        }
    },
    "additionalProperties": False
}


def validate_template(data):
    try:
        validate(data, template_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}