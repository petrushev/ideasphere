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
            u = User(service_id = profile_id, service = 'gmail')
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
