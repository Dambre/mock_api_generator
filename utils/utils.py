
from jsonschema import validate


def json_validate(json, json_validation_obj):
    valid = True
    error = {}
    try:
        validate(json, json_validation_obj)
    
    except Exception as e:
        valid = False
        error = {'error': '{}'.format(e)}

    return valid, error