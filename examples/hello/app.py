from glaso import get, post, delete, mount, all, use, dispatch, run, Response, catch

@get('^/$')
def home(x):
    return 'Hello'

@post('^/users/?$')
def create_user(req):
    return 201, {'id': 123}

@all('')
def notfound(x):
    return 404, 'Not really really found'

def throws(req):
    return 1/0

@get('/signup')
def signup(req):
    return 'Signed Up'

@post('/login')
def login(req):
    return 200, {'success': True}

@delete('/session')
def logout(req):
    return 200, {'success': True}

auth = [signup,
        login,
        logout]

routes = [
    home,
    create_user,
    mount('/auth', dispatch(auth)),
    notfound
]

middlewares = use(catch)
app = middlewares(dispatch(routes))

run(app)
