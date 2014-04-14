from werkzeug.routing import Map, Rule, EndpointPrefix

from ideasphere.controllers import index, login, admin, mission, user

routes = [
    Rule('/', endpoint=index.index),
    Rule('/login/g', defaults = {'original_url': ''}, endpoint = login.g_request, methods = ['GET']),
    Rule('/login/g/<path:original_url>', endpoint = login.g_request, methods = ['GET']),
    Rule('/login/callback/g', endpoint = login.g_callback, methods = ['GET']),
    Rule('/login/fb', defaults={'original_url': ''}, endpoint=login.fb_request, methods=['GET']),
    Rule('/login/fb/<path:original_url>', endpoint=login.fb_request, methods=['GET']),
    Rule('/login/callback/fb', defaults={'original_url': ''}, endpoint=login.fb_callback, methods=['GET']),
    Rule('/login/callback/fb/<path:original_url>', endpoint=login.fb_callback, methods=['GET']),
    Rule('/logout', endpoint=login.logout, methods=['GET']),
    Rule('/addmission', endpoint=admin.add_mission, methods=['GET']),
    Rule('/addmission', endpoint=admin.save_mission, methods=['POST']),
    Rule('/mission/<int:mission_id>', endpoint=mission.show, methods=['GET']),
    Rule('/mission/<int:mission_id>/addproblem', endpoint=admin.add_problem, methods=['GET']),
    Rule('/addproblem', endpoint=admin.save_problem, methods=['POST']),
    Rule('/problem/<int:problem_id>/submit', endpoint=user.submit_form, methods=['GET']),
    Rule('/submit', endpoint=user.save_proposal, methods=['POST']),
    Rule('/proposal/<int:proposal_id>', endpoint=mission.proposal, methods=['GET']),
    Rule('/vote/<int:proposal_id>/<int:vote_value>', endpoint=user.vote, methods=['GET']),
    Rule('/user/postcomment', endpoint=user.post_comment, methods=['POST']),
    Rule('/user/<int:user_id>', endpoint=user.profile, methods=['GET'])
]

url_map = Map(routes, strict_slashes = False)
