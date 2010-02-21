from inspect import getsourcefile
import os.path
import gobject

APIS = {}

class API(object):

    def emit_event(self, event, *args):

        def _emit():
            self.widget.js_context.events.fireEvent(event, *args)
            return False

        gobject.timeout_add(0, _emit)


def register(api):

    def decorator(api):
        path = os.path.abspath(getsourcefile(api))
        if not APIS.has_key(path):
            APIS[path] = {}
        APIS[path][name] = api
        return api

    if type(api) == str:
        name = api
        return decorator
    else:
        name = 'api'
        return decorator(api)
