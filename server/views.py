from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask.ext.login import login_required, login_user, current_user

from server.models import User
from server.forms import LoginForm, UserRegisterForm

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
        _res = db.session.query(User).filter(User.nickname==_u).first()
        if _res is None or not _res.verify_password(_p):
            flash('Warning: Username of password error')
            return redirect('/')
        flash('Login successful')
        session['username'] = request.form['username']
        return redirect('/')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirmpwd.data
        email = form.email.data

        # check whethre coordinations
        if password != confirm_password:
            flash("Warning: Password distinct")
            return redirect('/register')

        # check whethre the user exists
        res = db.session.query(User).filter(
                User.login_name == username).first()
        if res is not None:
            flash('Warning: User already exists')
            return redirect('/register')
        
        # check whethre the E-mail exists
        res = db.session.query(User).filter(
                User.email == email).first()
        if res is not None:
            flash('Warning: Email has been registered')
            return redirect('/register')

        user = User(login_name = username)
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()
        flash('Register successful')
        session['username'] = request.form['username']
        return redirect('/')
    return render_template('register.html', form = form)

