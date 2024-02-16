#!/usr/bin/python3i
"""
starts a Flask web application, hello hbnb, hbnb,
c is fun, python is fun, number, html num
"""

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    """returns HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C_is_fun(text):
    """display “C ” followed by the text variable"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """“Python ” will be followed by the text variable"""
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>')
def isa_Num(n):
    """display “n is a number” only if n is an integer"""
    n = str(n)
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def NT(n):
    """ display html !! only !! if n is intg"""
    n = str(n)
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
