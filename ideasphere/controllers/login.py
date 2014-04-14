from os import environ
from json import loads
from sys import stderr

import requests
from werkzeug.urls import url_encode, url_quote, url_decode
from werkzeug.utils import redirect

from ideasphere.db.models import User

G = {
    'client_id': environ['G_CLIENTID'],
    'client_secret': environ['G_SECRET'],
    'token_url': 'https://accounts.google.com/o/oauth2/auth',
    'access_url': 'https://accounts.google.com/o/oauth2/token'
}

FB = {
    'consumer_key': environ['FB_CONSUMER_KEY'],
    'consumer_secret': environ['FB_CONSUMER_SECRET']
}

def logout(request):
    if 'login' in request.client_session:
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

    service_id = content['id']

    # save userinfo by id
    u = User.save_g_data(request.session, service_id, fullname=content['name'], email=content['email'])
    u.img_url = content.get('picture')

    request.client_session['login'] = ['gmail', service_id]

    return redirect('/' + original_url)




def fb_request(request, original_url):
    original_url = request.host_url + 'login/callback/fb/' + url_quote(original_url)
    uri = 'https://www.facebook.com/dialog/oauth/?' + \
              url_encode({'client_id': FB['consumer_key'],
                          'redirect_uri': original_url})
    return redirect(uri)

def fb_callback(request, original_url):
    if 'code' not in request.args:
        return redirect('/?msg=2')

    code = request.args['code']
    callback_uri = request.host_url + 'login/callback/fb/' + url_quote(original_url)

    q = requests.get('https://graph.facebook.com/oauth/access_token?' + \
                     url_encode({'client_id': FB['consumer_key'],
                                 'redirect_uri': url_quote(callback_uri),
                                 'client_secret': FB['consumer_secret'],
                                 'code': code}))

    if q.status_code != 200:
        return redirect('/?msg=2')

    content = url_decode(q.content)
    access_token = content['access_token']

    q = requests.get("https://graph.facebook.com/me?access_token=" + access_token)

    if q.status_code != 200:
        return redirect('/?msg=2')

    userdata = loads(q.content)

    profile_id = userdata['id']
    email = userdata.get('email')
    fullname = userdata['name']

    img_url = None
    try:
        q = requests.get("https://graph.facebook.com/%s/picture?redirect=0" % profile_id)
        if q.status_code == 200:
            userdata = loads(q.content)['data']
            img_url = userdata['url']

    except Exception, exc:
        stderr.write('fb profile pic fetch error: ' + str(exc))

    # save userinfo by id
    u = User.save_fb_data(request.session, profile_id, fullname, email)
    u.img_url = img_url
    request.session.flush()

    # set redirect with cookie
    request.client_session['login'] = ['fb', profile_id]

    return redirect('/' + original_url)
