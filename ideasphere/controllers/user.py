from datetime import datetime
from functools import wraps

from lxml.html import fromstring
from werkzeug.utils import redirect
from sqlalchemy.orm.exc import NoResultFound

from ideasphere.forms import ProposalForm
from ideasphere.db.models import Problem, Proposal, Vote, Comment, User
from ideasphere.utils import return_json

def user(fc):
    @wraps(fc)
    def wrapped_fc(request, **kwargs):
        user = request.logged_user()
        if user is None:
            return {}, 'notfound.phtml', 404

        return fc(request, user, **kwargs)

    return wrapped_fc

def submit_form(request, problem_id):

    try:
        problem = Problem.load(request.session, id=problem_id)
    except NoResultFound:
        return {}, 'notfound.phtml', 404

    form = ProposalForm()
    form.problem_id.data = problem_id

    return {'form': form, 'problem': problem}, \
           'user/submit.phtml'

@user
def save_proposal(request, user):
    form = ProposalForm(request.form)

    try:
        problem = Problem.load(request.session, id=form.problem_id.data)
    except NoResultFound:
        return {}, 'notfound.phtml', 404

    img = request.files['img'].stream.read().encode('base64')
    model = request.files['model'].stream.read().encode('base64')

    proposal = Proposal(problem=problem,
                        submiter=user,
                        submited=datetime.utcnow(),
                        title=form.title.data,
                        description=form.description.data,
                        img=img,
                        model=model)
    request.session.flush()

    return redirect('/proposal/%d' % proposal.id)

@user
def vote(request, user, proposal_id, vote_value):
    try:
        proposal = Proposal.load(request.session, id=proposal_id)
    except NoResultFound:
        return return_json({})

    if proposal.user_id == user.id:
        return return_json({})
        
    
    try:
        vote = Vote.load(request.session, user_id=user.id, proposal_id=proposal.id)
    except NoResultFound:
        vote = Vote(voter=user, proposal=proposal)
        request.session.add(vote)

    vote.is_plus = (not vote_value == 0)

    return return_json({})


@user
def post_comment(request, user):
    proposal_id = int(request.form['proposal_id'])
    try:
        proposal = Proposal.load(request.session, id=proposal_id)
    except NoResultFound:
        return return_json({})

    content = request.form['content']
    content = fromstring(content).text.replace('\n', ' ')
    page_id = 'proposal/%d' % proposal.id

    comment = Comment(time=datetime.utcnow(), user=user,
                      page_id=page_id, content=content)
    request.session.add(comment)
    return return_json({'status': 'ok',
                        'content': 'content',
                        'user': {'id': user.id,
                                 'alias': user.alias}})

def profile(request, user_id):
    try:
        user = User.load(request.session, id=user_id)
    except NoResultFound:
        return

    return {'show_user': user}, 'profile.phtml'
