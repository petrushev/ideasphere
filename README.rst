Ideasphere
==========

Web site for Ideasphere project in NASA Space Apps Challenge:

Colaborative solutions for 3D printing in space mission problems

Staging on OpenShift: https://ideasphere-petrushev.rhcloud.com

Requirements
------------

- python 2.7
- postgresql >= 9.1
- psycopg2
- SQLAlchemy
- Jinja2
- Werkzeug
- lxml
- requests
- wtforms

Installation
------------

#. Create database and run ``db/rolling.sql``
#. Create data folder
#. Start static content server for path ``wsgi/static``
#. Register application on google console for login purposes
#. Fill the environ values in libs/run.py:

   - COOKIE_SECRET
   - OPENSHIFT_DATA_DIR
   - OPENSHIFT_POSTGRESQL_DB_URL
   - DBNAME
   - CDN
   - G_CLIENTID
   - G_SECRET
   - GOOGLE_SITE_VERIFICATION
