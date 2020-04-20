from invenio_app.factory import create_api

# APPLICATION_ROOT='/api' has to be set for this to work !

print('Application loading ...')


class PrefixMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path_info = environ['PATH_INFO']
        script = ''
        if path_info.startswith('/api'):
            script = '/api'
            path_info = path_info[4:]
        original_script_name = environ.get("SCRIPT_NAME", "")
        environ["SCRIPT_NAME"] = original_script_name + script
        environ["PATH_INFO"] = path_info
        return self.app(environ, start_response)


application = create_api()
application.wsgi_app = PrefixMiddleware(application.wsgi_app)
