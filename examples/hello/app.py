from glaso import App, run

app = App()

routes = [
    home,
    notfound
]

@app.get('/')
def home():
    return 'Hello'

@app.all()
def notfound():
    return '404 - Not Found'

run(app, port=3000)
