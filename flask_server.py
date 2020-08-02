
from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return 'index'


def init_flask():
    print("Building Flask app")
    app.run(debug=True, host='0.0.0.0', port=80)
