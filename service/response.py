from flask import jsonify, request


class Response:
    @classmethod
    def success(cls, status, data, status_code=200, message=None):
        response_dict = {
            'status': status,
            'data': data,
            'request_id': request.environ.get('HTTP_X_REQUEST_ID', 'NA')
        }
        if message:
            response_dict['message'] = message
        return jsonify(response_dict), status_code

    @classmethod
    def error(cls, error_code, message, status_code=500):
        response_dict = {
            'status': 'error',
            'error': message,
            'error_code': error_code,
            'request_id': request.environ.get('HTTP_X_REQUEST_ID', 'NA')
        }
        return jsonify(response_dict), status_code
