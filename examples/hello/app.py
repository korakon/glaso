from glaso import get, post, delete, mount, all, use, dispatch, run, Response, catch
from glaso.response import html, json

@get('^/$')
def home(x):
    return html('Hello')

@post('^/users/?$')
def create_user(req):
    return json({'id': 123}, status=201)

def notfound(x):
    return html('Not really really found', status=404)

def throws(req):
    return 1/0

@get('^/$')
def signup(req):
    return html('Signup')

@post('/login/?$')
def login(req):
    return json({'success': True})

@delete('/session/?$')
def logout(req):
    return json({'success': False})

auth = [signup,
        login,
        logout]

routes = [
    home,
    create_user,
    mount('/auth', dispatch(*auth)),
    notfound
]

middlewares = use(catch)
app = middlewares(dispatch(*routes))

if __name__ == '__main__':
    run(app, use_reloader=True)
