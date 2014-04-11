from setuptools import setup

setup(name='Ideasphere',
      version='1.0',
      description='Ideasphere',
      author='Baze Petrushev',
      author_email='b.petrushev@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['SQLAlchemy',
                        'psygopg2',
                        'Jinja2',
                        'Werkzeug'])
