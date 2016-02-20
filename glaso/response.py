from json import dumps
from werkzeug.wrappers import Response as Base
from uuid import UUID
from datetime import datetime
from werkzeug.http import http_date

class Response(Base):
    pass

def default(obj):
    if isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return http_date(obj)
    else:
        return json.JSONEncoder.default(self, obj)

def _dumps(obj, default=default):
    return dumps(obj, default=default)

def json(body, *args, **kwargs):
    return Response(_dumps(body), *args, content_type='application/json', **kwargs)

def html(body, *args, **kwargs):
    return Response(body, *args, content_type='text/html', **kwargs)
