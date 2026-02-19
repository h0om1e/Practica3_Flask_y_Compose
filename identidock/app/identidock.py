from flask import Flask, Response, request
import requests
import hashlib

app = Flask(__name__)

salt = "UNIQUE_SALT"
default_name = "Adrian"

@app.route('/', methods=['GET', 'POST'])
def index():
    name = default_name

    if request.method == 'POST':
        name = request.form['name']

    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    header = '<html><head><title>Identidock</title></head><body>'
    body = f'''
        <h1>Generador de Identicons</h1>
        <form method="POST">
            Introduce tu nombre:
            <input type="text" name="name" value="{name}">
            <input type="submit" value="Submit">
        </form>
        <p>Tu avatar:</p>
        <img src="/monster/{name_hash}">
    '''
    footer = '</body></html>'

    return header + body + footer


@app.route('/monster/<name>')
def get_identicon(name):
    r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
    image = r.content
    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
