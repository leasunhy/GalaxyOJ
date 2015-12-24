from datetime import datetime
from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask.ext.login import login_required, login_user, current_user, logout_user

from server.models import User, Problem
from server.forms import LoginForm, UserRegisterForm, EditProblemForm

from . import app, db, login_manager, q
from .models import *

__all__ = ['index']

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page = 1):
    notifs = Notification.query.paginate(page=page, per_page=20).items
    return render_template('index.html', posts=notifs)


@app.route('/solutions')
@app.route('/solutions/<int:page>')
def solutions(page = 1):
    solutions = Solution.query.paginate(page=page, per_page=20).items
    return render_template('solution_list.html', posts=solutions)


@app.route('/tutorials')
@app.route('/tutorials/<int:page>')
def tutorials(page = 1):
    tutorials = Tutorial.query.paginate(page=page, per_page=20).items
    return render_template('tutorial_list.html', posts=tutorials)


@app.route('/problems')
@app.route('/problems/<int:page>')
def list_problems(page = 1):
    problems = Problem.query.filter(Problem.visible==True)\
            .order_by(Problem.id).paginate(page=page, per_page=20).items
    return render_template('problems.html', problems=problems)


@app.route('/contests')
@app.route('/contests/<int:page>')
def list_contests(page = 1):
    contests = Contest.query.paginate(page=page, per_page=20).items
    return render_template('contests.html', contests=contests)


@app.route('/status')
@app.route('/status/<int:page>')
def list_status(page = 1):
    submissions = Submission.query.order_by(Submission.id.desc())\
                                  .paginate(page=page, per_page=20).items
    return render_template('status.html', submissions=submissions)


@app.route('/problem/<int:id>')
def problem(id=1):
    problem = Problem.query.get(id)
    return render_template('show_problem.html', p=problem)


@app.route('/contest/<int:id>')
def contest(id=1):
    contest = Contest.query.get(id)
    return render_template('show_contest.html', c=contest)


@app.route('/contest/<int:cid>/problems/<int:pid>')
def contest_problem(cid=1, pid=1):
    contest = Contest.query.get(cid)
    problem = contest.problems[pid-1]
    return render_template('show_problem.html', p=problem)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm(prefix='login-')
    if form.validate_on_submit():
        flash('Login successful')
        u = User.query.filter_by(login_name=form.username.data).first()
        login_user(u)
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/logout')
def user_logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/edit_problem/<int:pid>', methods=['GET', 'POST'])
@app.route('/edit_contest/<int:cid>/problem/<int:pid>', methods=['GET', 'POST'])
def edit_problem(cid = 0, pid = 0):
    # TODO (mstczuo <mstczuo@163.com>)
    #if current_user is None:
    #    return render_template('fatal.html', info="Please login first")
    #if current_user.privilege_level == 0:
    #    return render_template('fatal.html', info="Permission denied")
    if cid != 0:
        contest = Contest.query.get(cid)
        if not contest:
            flash('Contest (cid = %d) not found.' % cid)
            return redirect('/')
        try:
            prob = Problem() if pid == 0 else contest.problems[pid]
        except IndexError:
            flash('Contest (cid = %d) does not have %d-th problem.') % (cid, pid)
            return redirect('/')
        prob.visible = prob.visible or contest.end_time < datetime.now()
    else:
        prob = Problem() if pid == 0 else Problem.query.get(pid)
        prob.visible = True
    if prob is None:
        flash('Problem (pid = %d) not found.' % pid)
        return redirect('/')
    form = EditProblemForm(obj = prob)
    if form.validate_on_submit():
        form.populate_obj(prob)
        db.session.add(prob)
        db.session.commit()
        flash('Edit problem successful.')
        return redirect('/problems')
    return render_template('edit_problem.html', form=form, pid=pid, cid=cid)


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

