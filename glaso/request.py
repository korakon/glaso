from werkzeug.wrappers import Request as Base

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
            'params': self.params,
            'prefix': self.prefix,
            'files': self.files,
            'cookies': self.cookies
        }
