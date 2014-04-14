from json import loads, dumps

from werkzeug.urls import url_quote
from sqlalchemy.sql.expression import func, and_, not_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.util import aliased
from sqlalchemy.orm import eagerload

from ideasphere.db import BaseModel

class User(BaseModel):

    @staticmethod
    def save_g_data(session, profile_id, fullname, email):
        try:
            u = User.load(session, service_id = profile_id, service = 'gmail')

        except NoResultFound:
            u = User(service_id=profile_id, service='gmail', is_admin=True)
            session.add(u)
            session.flush()

        u.fullname = fullname
        u.display_name = fullname
        u.email = email

        return u

    @staticmethod
    def save_fb_data(session, service_id, fullname, email):
        try:
            u = User.load(session, service_id=service_id, service='fb')

        except NoResultFound:
            u = User(service_id=service_id, service='fb', is_admin=True)
            session.add(u)
            session.flush()

        u.fullname = fullname
        u.display_name = fullname
        u.email = email

        return u

    @property
    def alias(self):
        if self.display_name is not None:
            return self.display_name

        if self.service == 'gmail':
            return self.fullname

        raise NotImplementedError, ' for service ' + self.service

    @property
    def alias_repr(self):
        return url_quote(self.alias.replace(' ', '_'))

    @property
    def home_url(self):
        raise NotImplementedError, ' for service ' + self.service

def json_property(json, field):
    if json is None:
        return None
    try:
        json = loads(json)
        return json.get(field)
    except ValueError:
        return None

def prepare_json_property(existing, field, value):
    if existing is None:
        json = {}
    else:
        try:
            json = loads(existing)
        except ValueError:
            json = {}

    json[field] = value
    return dumps(json)

class Mission(BaseModel):

    @property
    def description(self):
        return json_property(self.meta, 'description')

    @description.setter
    def description(self, value):
        self.meta = prepare_json_property(self.meta, 'description', value)


class Problem(BaseModel):

    @property
    def description(self):
        return json_property(self.meta, 'description')

    @description.setter
    def description(self, value):
        self.meta = prepare_json_property(self.meta, 'description', value)

class Proposal(BaseModel):
    
    def score(self):
        return sum([1 if vote.is_plus else -1
                    for vote in self.votes])

    @property
    def comments(self):
        if not hasattr(self, 'id') or self.id is None:
            return []
        page_id = 'proposal/%d' % self.id
        return self.session.query(Comment)\
                   .filter(Comment.page_id == page_id)\
                   .order_by(Comment.time.desc()).all()

class Vote(BaseModel):
    pass

class Comment(BaseModel):
    pass
