
class Route:
    def __init__(self, method, pattern, callback):
        self.method = method
        self.pattern = pattern
        self.callback = callback

class App:
    def __init__(self):
        self.routes = []

    def route(self, method, pattern):
        def wrapper(route):
            self.routes.append(Route(method, pattern, callback))
        return wrapper

    def get(self, pattern):
        return self.route(self, method='GET', pattern)

    def all(self, pattern):
        return self.route(self, method='*', pattern)
