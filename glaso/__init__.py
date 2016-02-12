from glaso import Routes, use, middleware
from glaso.x import session

app = App()

@app.get('/')
def home(x):
    return 'Hello world!'

@app.post('/users/')
def users(x):
    return 201, {'id': 1234}

@app.put('/users/:username')
def putusers(db, params, session, cookies):
    user = db.User.get(params.username)
    return 201, {'success': True}

@middleware
def cors(app):
    def wrapper(ctx):
        response = app(ctx)
        response.headers['Access-Allow-Origin'] = '*'

middlewares = use(error, cors, session)
app = middlwares(app)

if __name__ == '__main__':
    run(app, port=3000)
