from inspect import getsourcefile
import os.path
import gobject
import threading

APIS = {}

class Thread(threading.Thread):

    def __init__(self, func, args=[], kwargs={}, callback=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.callback = callback

        threading.Thread.__init__(self)


    def run(self):

        ret = self.func(*self.args, **self.kwargs)

        if self.callback:
            if type(ret) == tuple:
                gobject.idle_add(self._call_callback, self.callback, *ret)
            else:
                gobject.idle_add(self._call_callback, self.callback, ret)


    def foo(self, *args):

        print args


    def _call_callback(self, callback, *args):

        callback(*args)
        return False


class API(object):
    def __init__(self):
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
