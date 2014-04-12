from functools import wraps
from datetime import datetime

from ideasphere.forms import AddMissionForm, AddProblemForm
from ideasphere.db.models import Mission, Problem
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import redirect

def admin(fc):
    @wraps(fc)
    def wrapped_fc(request, **kwargs):
        user = request.logged_user()
        if user is None or not user.is_admin:
            return {}, 'notfound.phtml', 404

        return fc(request, user, **kwargs)

    return wrapped_fc

@admin
def add_mission(request, user):
    form = AddMissionForm()
    return {'form': form}, 'admin/addmission.phtml'

@admin
def save_mission(request, user):
    form = AddMissionForm(request.form)

    title = form.title.data
    description = form.description.data

    try:
        Mission.load(request.session, title=title)
        return {'form': form, 'error': 'Mission already exists'}, \
                'admin/addmission.phtml'
    except NoResultFound:
        mission = Mission(title=title, description=description, created=datetime.utcnow())
        request.session.add(mission)
        return redirect('/')

@admin
def add_problem(request, user, mission_id):
    try:
        mission = Mission.load(request.session, id=mission_id)
    except NoResultFound:
        return {}, 'notfound.phtml', 404

    form = AddProblemForm()
    form.mission_id.data = mission.id
    return {'form': form,
            'mission': mission}, 'admin/addproblem.phtml'

@admin
def save_problem(request, user):
    form = AddProblemForm(request.form)
    try:
        mission = Mission.load(request.session, id=form.mission_id.data)
    except NoResultFound:
        return {}, 'notfound.phtml', 404

    title = form.title.data
    description = form.description.data

    try:
        Problem.load(request.session, title=title, mission_id=mission.id)
        return {'form': form, 'mission': mission,
                'error': 'Problem already reported'}, \
               'admin/addproblem.phtml'
    except NoResultFound:
        Problem(title=title, mission=mission,
                          description=description, created=datetime.utcnow())
        return redirect('/mission/%d' % mission.id)
