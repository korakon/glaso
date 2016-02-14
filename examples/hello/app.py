from glaso import get, post, all, use, dispatch, run, Response, catch

@get('/')
def home(req):
    return 'Hello'

@post('/users/')
def create_user(req):
    return 201, {'id': 123}

@all()
def notfound(req):
    return 404, 'Not really really found'

def throws(req):
    return 1/0

routes = [
    home,
    create_user,
    throws,
    notfound
]

middlewares = use(catch)
app = middlewares(dispatch(routes))

run(app)
