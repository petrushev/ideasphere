from os import environ
from json import loads
from sys import stderr

import requests
from werkzeug.urls import url_encode
from werkzeug.utils import redirect

from ideasphere.db.models import User

G = {
    'client_id': environ['G_CLIENTID'],
    'client_secret': environ['G_SECRET'],
    'token_url': 'https://accounts.google.com/o/oauth2/auth',
    'access_url': 'https://accounts.google.com/o/oauth2/token'
}

def logout(request):
    del request.client_session['login']
    return redirect('/')

def g_request(request, original_url):
    query_string = url_encode({'client_id': G['client_id'],
                               'response_type': 'code',
                               'scope': 'openid email profile',
                               'redirect_uri': request.host_url + 'login/callback/g',
                               'state': original_url,
                               'access_type': 'online'})
    # redirects to 'login with google+' page
    return redirect(G['token_url'] + '?' + query_string)

def g_callback(request):
    # parse the original url from the google+ redirect state param
    original_url = request.args.get('state', '')
    code = request.args['code']

    # authenticate the passed code
    q = requests.post(G['access_url'],
                      data = {'code': code,
                              'client_id': G['client_id'],
                              'client_secret': G['client_secret'],
                              'redirect_uri': request.host_url + 'login/callback/g',
                              'grant_type': 'authorization_code'})

    if q.status_code != 200:
        stderr.write("Login error G+:\n    %s\n" % q.content)
        return redirect('/?msg=AUTH_ERROR')

    content = loads(q.content)
    access_token = content['access_token']
    del content

    # get userinfo
    q = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + access_token)
    content = loads(q.content)

    profile_id = content['id']

    # save userinfo by id
    User.save_g_data(request.session, profile_id, fullname=content['name'], email=content['email'])

    request.client_session['login'] = ['gmail', profile_id]

    return redirect('/' + original_url)
