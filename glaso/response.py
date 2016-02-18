from werkzeug.wrappers import Response as Base
from json import dumps

class Response(Base):
    pass

def json(body, *args, **kwargs):
    return Response(dumps(body), *args, content_type='application/json', **kwargs)

def html(body, *args, **kwargs):
    return Response(body, *args, content_type='text/html', **kwargs)
