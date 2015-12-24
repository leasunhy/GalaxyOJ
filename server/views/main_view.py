from . import main
from flask import redirect, url_for

@main.route('/')
@main.route('/index')
def index():
    return redirect(url_for('post.notifications'))

