from flask import render_template, url_for, request, redirect, flash, jsonify
from flask.ext.login import login_required, login_user, current_user

from . import app, db, login_manager

__all__ = ['index']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#@app.route('/login')
#def login():
#    return render_template('login.html')
