import sys
from os import environ
from os.path import join as pathjoin
import json

from werkzeug.utils import cached_property
from werkzeug.wrappers import BaseRequest, Response
from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.exceptions import HTTPException
from werkzeug.urls import url_quote

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from jinja2.bccache import FileSystemBytecodeCache

from sqlalchemy.orm.exc import NoResultFound

from ideasphere import project_path
from ideasphere.controllers import index
from ideasphere.db.mappers import Session
from ideasphere.db.models import User
from ideasphere.routes import url_map


CDN = environ['CDN']
COOKIE_SECRET = environ['COOKIE_SECRET']
TEMPLATES_AUTORELOAD = int(environ['TEMPLATES_AUTORELOAD'])
DATA_DIR = environ['OPENSHIFT_DATA_DIR']

class JsonSecureCookie(SecureCookie):
    serialization_method = json

class Request(BaseRequest):

    should_rollback = False

    @cached_property
    def client_session(self):
        data = self.cookies.get('session_data')
        if not data:
            return JsonSecureCookie(secret_key=COOKIE_SECRET)

        return JsonSecureCookie.unserialize(data, COOKIE_SECRET)

    def logged_user(self):
        try:
            service, service_id = self.client_session['login']
            return User.load(self.session,
                             service=service, service_id=service_id)

        except (KeyError, NoResultFound, ValueError):
            return None

def prepare_response(tpl_env, raw_response):
    if type(raw_response) is Response:
        return raw_response

    if len(raw_response) > 3:
        raise ValueError

    view, template = raw_response[:2]

    response = Response('', content_type = "text/html; charset=UTF-8")

    response.data = tpl_env.get_template(template).render(**view)
    response.content_length = len(response.data)

    if len(raw_response) == 3:
        response.status_code = raw_response[2]
    else:
        response.status_code = 200

    return response


class Application(object):

    def __init__(self):
        self.appspace = {}
        self.url_map = url_map

        templates = pathjoin(project_path, 'templates')
        template_cache = DATA_DIR + 'template_cache'

        self.tpl_env = Environment(loader=FileSystemLoader(templates),
                                   bytecode_cache=FileSystemBytecodeCache(template_cache),
                                   auto_reload=TEMPLATES_AUTORELOAD)
        self.tpl_env.globals.update({'url_quote': url_quote,
                                     'cdn': CDN})

    def get_response(self, environ):
        urls = self.url_map.bind_to_environ(environ)

        session = Session()

        request = Request(environ)
        request.session = session
        request.app = self

        try:
            endpoint, args = urls.match()
        except HTTPException, exc:
            sys.stderr.write('Routing error:\n    %s\n' % str(exc))
            raw_response = index.notfound(request)
        else:
            raw_response = endpoint(request, **args)

        if type(raw_response) is not Response:
            view = {'user': request.logged_user(),
                    'path': request.path}
            view.update(raw_response[0])
            raw_response = (view,) + raw_response[1:]

        response = prepare_response(self.tpl_env, raw_response)

        if request.should_rollback:
            session.rollback()
        else:
            session.commit()

        if request.client_session.should_save:
            session_data = request.client_session.serialize()
            response.set_cookie('session_data', session_data,
                                httponly=True)
        return response


    def __call__(self, environ, start_response):
        response = self.get_response(environ)
        return response(environ, start_response)
