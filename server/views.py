from flask import render_template, url_for, request, redirect, flash, jsonify
from flask.ext.login import login_required, login_user, current_user

from server.models import User
from server.forms import LoginForm

from . import app, db, login_manager

__all__ = ['index']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        _u = form.username.data
        _p = form.password.data
        _res = db.session.query(User).filter(User.nickname==_u).all()
        if _res == []:
            flash('Warning: User not found')
            return redirect('/')
        if not _res[0].verify(_p):
            flash('Incorrect password')
            return redirect('/')
        flash('Login successful')
        session['username'] = request.form['username']
        return redirect('/')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
