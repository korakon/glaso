from functools import wraps, reduce
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

# transform routes' return values into a Response object
# return 202
# return body
# return status, body
# return status, headers, body

def transform(value):
    if isinstance(value, int):
        return Response('', status=value)
    elif isinstance(value, str):
        return Response(value)
    elif len(value) == 2:
        status, body = value
        return Response(body, status)
    elif len(value) == 3:
        status, headers, body = value
        return Response(body, status, headers)
    else:
        raise ValueError('Unknown return type: {}, value: {}'\
                         .format(type(value), value))

def route(pattern, method):
    def router(callback):
        @wraps(callback)
        def wrapper(req):
            if not pattern or req.path == pattern:
                return transform(callback(req))
            else:
                return None
        return wrapper
    return router

def make(method):
    def wrapper(pattern=''):
        return route(pattern, method)
    return wrapper

get = make('GET')
post = make('POST')
delete = make('DELETE')
put = make('PUT')
patch = make('PATCH')
options = make('OPTIONS')
all = make('*')

def use(*middlewares):
    def run(app):
        return reduce(lambda x, f: f(x), middlewares[::-1], app)
    return run

def dispatch(routes):
    def wrapper(*args, **kw):
        for route in routes:
            res = route(*args, **kw)
            if isinstance(res, Response):
                return res
        else:
            return Response("Not Found", status=404, mimetype='text/plain')
    return wrapper

def bridge(app):
    @wraps(app)
    def wrapper(environ, start):
        request = Request(environ)
        response = app(request)
        return response(environ, start)
    return wrapper

def catch(app):
    @wraps(app)
    def middleware(req):
        try:
            response = app(req)
            return response
        except Exception as e:
            print(e)
            return Response("Shit happened", status=500, mimetype='text/plain')
    return middleware


def run(app, host='localhost', port=4000):
    return run_simple(host, port, bridge(app))
