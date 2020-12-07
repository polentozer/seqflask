from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '7be64ed4f35ea8c568e4f8603f346920'

from flask_seq import routes

