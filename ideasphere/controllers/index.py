from os import environ
from ideasphere.db.models import Mission, Problem

GOOGLE_SITE_VERIFICATION = environ['GOOGLE_SITE_VERIFICATION']

def index(request):
    missions = request.session.query(Mission)\
                      .order_by(Mission.created.desc()).all()
    problems = request.session.query(Problem)\
                      .order_by(Problem.created.desc()).limit(6).all()

    return {'google_site_verification': GOOGLE_SITE_VERIFICATION,
            'missions': missions, 'problems': problems}, \
           'index.phtml'

def notfound(request):
    return {}, 'notfound.phtml', 404

def about_us(request):
    return {}, 'aboutus.phtml', 404
