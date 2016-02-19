import re
from functools import wraps, reduce
from werkzeug.serving import run_simple
from .route import Route
from .request import Request
from .response import Response

def make(methods=[]):
    def router(pattern, name=None):
        def wrapper(callback):
            return Route(pattern, callback, name, methods)
        return wrapper
    return router

get = make(['GET', 'HEAD'])
post = make(['POST'])
delete = make(['DELETE'])
put = make(['PUT'])
patch = make(['PATCH'])
options = make(['OPTIONS'])
all = make()

def use(*middlewares):
    def run(app):
        return reduce(lambda x, f: f(x), middlewares[::-1], app)
    return run

def dispatch(*routes):
    def wrapper(*args, **kw):
        for route in routes:
            res = route(*args, **kw)
            if isinstance(res, Response):
                return res
    return wrapper

def bridge(app):
    @wraps(app)
    def wrapper(environ, start):
        request = Request(environ)
        response = app(request)
        response.headers["Server"] = "G L A S O"
        return response(environ, start)
    return wrapper

def catch(app):
    @wraps(app)
    def middleware(req):
        try:
            response = app(req)
            return response
        except Exception as e:
            raise e
            return Response("Shit happened", status=500, mimetype='text/plain')
    return middleware

def mount(path, handler):
    prefix = re.compile(path)

    @wraps(handler)
    def wrapper(req):
        to_match = req.prefix[-1] if len(req.prefix) else req.path
        m = prefix.match(to_match)
        if m:
            req.prefix.append(prefix.split(to_match)[-1])
            req.params.update(m.groupdict())
            try:
                res = handler(req)
                return res
            finally:
                req.prefix.pop()
        else:
            return None
    return wrapper

def run(app, host='localhost', port=4000, *args, **kwargs):
    return run_simple(host, port, bridge(app), *args, **kwargs)
