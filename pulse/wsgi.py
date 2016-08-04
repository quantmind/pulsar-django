from pulsar.apps.wsgi import (LazyWsgi, WsgiHandler,
                              wait_for_body_middleware,
                              middleware_in_executor)
from pulsar.utils.importer import module_attribute


class Wsgi(LazyWsgi):
    '''The Wsgi middleware used by the django ``pulse`` command
    '''
    cfg = None

    def setup(self, environ=None):
        '''Set up the :class:`.WsgiHandler` the first time this
        middleware is accessed.
        '''
        from django.conf import settings
        from django.core.wsgi import get_wsgi_application
        #
        try:
            dotted = settings.WSGI_APPLICATION
        except AttributeError:  # pragma nocover
            dotted = None
        if dotted:
            app = module_attribute(dotted)
        else:
            app = get_wsgi_application()
        app = middleware_in_executor(app)
        return WsgiHandler((wait_for_body_middleware, app))
