from flask import Flask, send_file
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    # Automatically run the integration process (or just show result)
    subprocess.run(["python3", "main.py"])
    return send_file("output.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
