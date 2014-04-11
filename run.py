from os import environ

try:
    import additional_env
except ImportError:
    pass

environ.update({
  'TEMPLATES_AUTORELOAD': '1'
})

from ideasphere.app import Application

application = Application()

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple("localhost", 8090,
               application, use_reloader = True, threaded = False, processes = 1)
