from flask import request, jsonify, abort

from listener import app
from .routing import get_route


@app.route('/', methods=['POST'])
def index():
    print(request.json)
    if not request.is_json:
        return jsonify({'error': 400, 'errorMsg': 'request is not json'})
    return jsonify(validate_post_data(request.json))


def validate_post_data(data):
    id = data.get('msgId', '')
    if not id:
        return {
            'error': 400,
            'errorMsg': 'msgId is not provided'
        }

    _route = get_route(id)
    if not _route:
        return {
            'error': 400,
            'errorMsg': 'msgId is invalid'
        }

    return _route(data).get_response()
