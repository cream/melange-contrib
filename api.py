from inspect import getsourcefile
import os.path
import gobject
import threading

APIS = {}

class Thread(threading.Thread, gobject.GObject):

    __gtype_name__ = 'Thread'
    __gsignals__ = {
        'finished': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        }

    def __init__(self, func, args=[], kwargs={}):
        self.func = func
        self.args = args
        self.kwargs = kwargs

        threading.Thread.__init__(self)
        gobject.GObject.__init__(self)


    def run(self):

        ret = self.func(*self.args, **self.kwargs)

        #if type(ret) != tuple:
        #    ret = (ret,)

        print ret

        self.emit('finished', ret)


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
