import os
from flask import Flask, send_file, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # HTML template to display the image with some style
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Seamless Person Integration</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
                background-color: #f5f5f5;
            }
            img {
                max-width: 90%;
                height: auto;
                border: 2px solid #333;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>Seamless Person Integration Result</h1>
        <img src="/image" alt="Output Image">
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/image')
def image():
    path_to_file = os.path.join(os.getcwd(), 'results', 'blended_output.jpg')
    
    if not os.path.exists(path_to_file):
        return "<h1>Image not found!</h1>", 404
    
    return send_file(path_to_file, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
