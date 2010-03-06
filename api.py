import os.path
import gobject
from inspect import getsourcefile
from collections import defaultdict

APIS = defaultdict(dict)

class API(object):
    def __init__(self, widget):
        pass

    def emit_event(self, event, *args):
        """ Emit the given event. """

        def _emit():
            self.widget.js_context.events.fireEvent(event, *args)
            return False

        gobject.timeout_add(0, _emit)


def register(api):
    """ Register an API object. """

    def decorator(api):
        path = os.path.abspath(getsourcefile(api))
        APIS[path][name] = api
        return api

    if isinstance(api, str):
        name = api
        return decorator
    else:
        name = 'api'
        return decorator(api)
