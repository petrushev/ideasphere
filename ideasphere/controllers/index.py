from os import environ

GOOGLE_SITE_VERIFICATION = environ['GOOGLE_SITE_VERIFICATION']

def index(request):
    return {'google_site_verification': GOOGLE_SITE_VERIFICATION}, \
           'index.phtml'

def notfound(request):
    return {}, 'notfound.phtml', 404
