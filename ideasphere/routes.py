from werkzeug.routing import Map, Rule, EndpointPrefix

from ideasphere.controllers import index, login

routes = [
    Rule('/', endpoint=index.index),
    Rule('/login/g', defaults = {'original_url': ''}, endpoint = login.g_request, methods = ['GET']),
    Rule('/login/g/<path:original_url>', endpoint = login.g_request, methods = ['GET']),
    Rule('/login/callback/g', endpoint = login.g_callback, methods = ['GET']),
    Rule('/logout', endpoint = login.logout, methods = ['GET'])
]

url_map = Map(routes, strict_slashes = False)
