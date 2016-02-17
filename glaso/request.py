from werkzeug.wrappers import Request as Base

class Request(Base):
    def __init__(self, environ):
        super(Request, self).__init__(environ)
        # Params captured from request url
        self.params = {}
        # User editable dictionary to pass values between routes.
        self.vault = {}
        # Used to mount apps
        # eg: mount('/api/users', users.app)
        self.prefix = []
