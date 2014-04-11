from json import dumps
from werkzeug.wrappers import Response

def return_json(view):
    response = Response('', content_type = "text/html; charset=UTF-8")
    response.data = json.dumps(view)
    response.content_length = len(response.data)
    response.content_type = "application/json"
    return response
