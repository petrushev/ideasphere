from os import environ
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relationship, backref, column_property
from sqlalchemy.sql.expression import and_
#from sqlalchemy.event import listen

from ideasphere.db import reflect
from ideasphere.db import models

conn_str = environ['OPENSHIFT_POSTGRESQL_DB_URL'] + '/' + environ['DBNAME']
engine = create_engine(conn_str)

## The commented lines provide hook for `connection_start` event
## Useful for patching custom composite types onto psycopg
#def connection_start_hook(dbapi_con, connection_record):
#    pass

#listen(engine, 'connect', connection_start_hook)

mappers, tables, Session = reflect(engine, models)

mappers['Mission'].add_properties({
    'problems': relationship(models.Problem,
                             order_by=models.Problem.created.desc(),
                             backref='mission')})

mappers['Problem'].add_properties({
    'proposals': relationship(models.Proposal,
                              order_by=models.Proposal.submited.desc(),
                              backref='problem')})

mappers['Proposal'].add_properties({
    'submiter': relationship(models.User, lazy='joined',
                             backref=backref('proposals',
                                             order_by=models.Proposal.submited.desc(),
                                             lazy='dynamic'))
})

mappers['Vote'].add_properties({
    'voter': relationship(models.User, lazy='joined'),
    'proposal': relationship(models.Proposal, lazy='joined',
                             backref='votes')
})

mappers['Comment'].add_properties({
    'user': relationship(models.User, lazy='joined')
})
