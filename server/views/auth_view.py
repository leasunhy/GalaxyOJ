from . import auth

from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask.ext.login import login_required, login_user, current_user, logout_user
from .. import app, db, login_manager
from ..models import User
from ..forms import LoginForm, UserRegisterForm

@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm(prefix='login-')
    if form.validate_on_submit():
        flash('Login successful')
        u = User.query.filter_by(login_name=form.username.data).first()
        login_user(u)
        return redirect('/')
    return render_template('login.html', form=form)


@auth.route('/logout')
def user_logout():
    session.clear()
    logout_user()
    return redirect('/')


@auth.route('/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('Register successful')
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=form)


