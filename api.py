#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import inspect
import os.path
import weakref
import gobject
import threading

APIS = {}

class Proxy(object):
    """
    A proxy for wrapping functions to run them in threads.
    This object registers potential callback functions
    and calls them using Mootools' Events.
    """

    def __init__(self, obj, ctx):
        """
        Initialize the Proxy object.

        :param obj: The function to wrap.
        :param ctx: A JavaScriptCore context.
        """

        self.obj = obj
        self.ctx_ref = weakref.ref(ctx)

        self.handler = None


    def __call__(self, *args):
        """ Call the wrapped function in another thread. """

        # Get callback function...
        args = list(args)

        func_args = inspect.getargspec(self.obj).args
        if (len(func_args) == len(args) and func_args[0] != 'self') or len(func_args) > len(args):
            callback = None
        else:
            callback = args[-1]
            del args[-1]

        # Initialize thread:
        t = Thread(self.obj, args)

        # Register callback function:
        if callback:
            ctx = self.ctx_ref()
            self.handler = ctx.widget.api.addEvent(self.obj.__name__, callback)
            t.connect('finished', lambda t, data: self.fire_event(self.obj.__name__, data))

        # Start thread:
        t.start()


    def fire_event(self, event, data):
        """
        Fire the given event.

        :param event: Name of the event to fire.
        :param data: Data to emit with the event.
        """

        ctx = self.ctx_ref()
        ctx.widget.api.fireEvent(self.obj.__name__, data)
        if self.handler:
            ctx.widget.api.removeEvent(self.obj.__name__, self.handler)
            self.handler = None


class PyToJSInterface(object):
    """
    The actual object being registered on the JavaScript-side of the life;)
    This tries to get exposed methods from the API object and yield it to JS.
    """

    def __init__(self, api):

        self.api = api


    def __getattribute__(self, obj_name):

        api = object.__getattribute__(self, 'api')
        obj = api.__getattribute__(obj_name)
        try:
            if isinstance(obj, Proxy):
                return obj
        except:
            pass
        raise AttributeError


class Thread(threading.Thread, gobject.GObject):
    """ An advanced threading class emitting a GObject signal after running. """

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
        """ The function getting called on ``Thread.start()``. """

        ret = self.func(*self.args, **self.kwargs)
        gobject.timeout_add(0, self._emit, ret)


    def _emit(self, ret):
        self.emit('finished', ret)


class API(object):
    """ The API object to subclass when writing a Python API for JS widgets. """

    def __init__(self):
        pass

    def emit(self, event, *args):
        """
        Emit an event with the given name and params.

        :param event: The event's name.
        :param args: A `list` or `tuple` of arguments.
        """

        self._js_ctx.widget.api.fireEvent(event, *args)


    def __getattribute__(self, obj_name):

        obj = object.__getattribute__(self, obj_name)
        try:
            if obj._callable:
                return Proxy(obj, self._js_ctx)
        except:
            pass
        return obj


class FunctionInMainThread(object):
    """ A wrapper for functions that have to be called in the main thread. """

    def __init__(self, func):

        self.func = func
        self.lock = threading.Event()
        self.ret = None


    def __call__(self, *args, **kwargs):

        self.lock.clear()
        gobject.timeout_add(0, self._func_wrapper, args, kwargs)
        self.lock.wait()
        return self.ret


    def _func_wrapper(self, args, kwargs):
        self.ret = self.func(*args, **kwargs)
        self.lock.set()


def in_main_thread(func):
    """ Decorator for functions that have to be called in the main thread. """

    def wrapper(*args, **kwargs):
        f = FunctionInMainThread(func)
        return f(*args, **kwargs)

    return wrapper


def register(api):
    """ Register the given API object. """

    def decorator(api):
        path = os.path.abspath(inspect.getsourcefile(api))
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


def expose(func):
    """ Expose the given function to JS. """

    func._callable = True
    return func
