import re
from .response import Response

class Route(object):
    """
    pattern=None means match any pattern
    methods=None means match any method
    """
    def __init__(self, pattern, callback, name=None, methods=None):
        self.regex = re.compile(pattern)
        self.name = name or callback.__name__
        self.callback = callback
        self.methods = methods or []

    def transform(self, value):
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


    def __call__(self, req):
        if req.method not in self.methods:
            return None
        prefix = "".join(req.prefix) if req.prefix else req.path
        matches = self.regex.match(prefix)
        if not matches:
            return None
        req.params.update(matches.groupdict())
        return self.transform(self.callback(req))

    def __str__(self):
        return "<Route {methods:20s} {regex:20s} {callback}>"\
            .format(methods=", ".join(self.methods),
                    regex=self.regex.pattern,
                    callback=self.name)
