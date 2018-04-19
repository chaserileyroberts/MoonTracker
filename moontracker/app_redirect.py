"""Redirect http to https."""
from flask import Flask, request, redirect

app = Flask(__name__)


@app.before_request
def before_request():
    """Redirect to https."""
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


app.run("0.0.0.0", port=5050)
