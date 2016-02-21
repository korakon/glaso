from werkzeug.wrappers import Request as Base
from functools import lru_cache
from json import loads

class Request(Base):
    def __init__(self, environ):
        super(Request, self).__init__(environ)
        # Params captured from request url
        self.params = {}
        # Used to mount apps
        # eg: mount('/api/users', users.app)
        self.prefix = []
        # User editable dictionary to pass values between routes.
        self.vault = {
            'request': self,
            'data': self.data,
            'params': self.params,
            'prefix': self.prefix,
            'files': self.files,
            'cookies': self.cookies
        }

    @property
    @lru_cache(10)
    def body(self):
        if self.mimetype == 'application/json':
            try:
                return loads(self.get_data(as_text=True))
            except ValueError:
                raise ValueError('Request body is not valid json')
        else:
            raise ValueError('Request body couldnt be decoded')
