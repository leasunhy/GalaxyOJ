from flask import render_template, url_for, request, redirect, flash, jsonify
from flask.ext.login import login_required, login_user, current_user

from . import app, db, login_manager, q

__all__ = ['index']

@app.route('/')
@app.route('/index')
def index():
    return 'Success!'

def hello_world(word):
    for i in range(18):
        print("Haha")

@app.route('/test')
def test():
    # get url that the person has entered
    job = q.enqueue_call(
        func=hello_world, args=("haha",), result_ttl=5000
    )
    print(job.get_id())
    return redirect('/')

