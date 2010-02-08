from inspect import getsourcefile
import os.path

APIS = {}

class WidgetAPI(object):
    pass


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
