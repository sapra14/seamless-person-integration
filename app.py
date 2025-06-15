import os
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    # Assuming output.png is in the same folder as app.py
    path_to_file = os.path.join(os.path.dirname(__file__), 'output.png')
    return send_file(path_to_file, mimetype='image/png')
