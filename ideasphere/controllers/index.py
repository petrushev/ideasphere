from os import environ
from ideasphere.db.models import Mission

GOOGLE_SITE_VERIFICATION = environ['GOOGLE_SITE_VERIFICATION']

def index(request):
    missions = request.session.query(Mission)\
                      .order_by(Mission.created.desc()).all()

    return {'google_site_verification': GOOGLE_SITE_VERIFICATION,
            'missions': missions}, \
           'index.phtml'

def notfound(request):
    return {}, 'notfound.phtml', 404
