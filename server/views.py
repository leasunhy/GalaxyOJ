from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask.ext.login import login_required, login_user, current_user

from server.models import User
from server.forms import LoginForm, UserRegisterForm

from . import app, db, login_manager, q
from .models import *

__all__ = ['index']

@app.route('/')
@app.route('/index')
def index():
    page = int(request.args.get('page', '1'))
    notifs = Notification.query.paginate(page=page, per_page=20).items
    return render_template('index.html', notifs=notifs)


@app.route('/problems')
@app.route('/problems/<int:page>')
def list_problems(page=1):
    problems = Problem.query.filter(Problem.visible==True)\
                            .paginate(page=page, per_page=20).items
    return render_template('problems.html', problems=problems)


@app.route('/problem/<int:id>')
def problem(id=1):
    problem = Problem.query.get(id)
    return render_template('show_problem.html', p=problem)


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
def user_logout():
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

def hello_world(word):
    for i in range(18):
        print("Haha")

@app.route('/test')
def test(submission_id):
    # get url that the person has entered
    job = q.enqueue_call(
        #TODO
        func=hello_world, args=("haha",), result_ttl=5000
    )
    print(job.get_id())
    return redirect('/')

