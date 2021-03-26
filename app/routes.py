from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Oieh, Flask is working!"
