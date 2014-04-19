from ideasphere.db.models import Mission, Proposal, Vote, Problem
from sqlalchemy.orm.exc import NoResultFound

def show(request, mission_id):
    try:
        mission = Mission.load(request.session, id=mission_id)
    except NoResultFound:
        return {}, 'notfound.phtml', 404
    
    return {'mission': mission}, \
           'mission.phtml'

def proposal(request, proposal_id):
    try:
        proposal = Proposal.load(request.session, id=proposal_id)
    except NoResultFound:
        return {}, 'notfound.phtml', 404

    problem = proposal.problem

    img64 = proposal.img

    model = proposal.model
    if model is not None:
        model = model.decode('base64')

    user = request.logged_user()
    if user is None:
        vote = None
    else:
        try:
            vote = Vote.load(request.session, proposal_id=proposal.id, user_id=user.id)
        except NoResultFound:
            vote = None

    view = {'problem': problem, 'proposal': proposal, 'vote': vote,
            'img64': img64, 'model': model}
    return view, 'proposal.phtml'

def recent_problems(request):
    problems = request.session.query(Problem).order_by(Problem.created.desc()).all()
    return {'problems': problems}, 'recentproblems.phtml'
