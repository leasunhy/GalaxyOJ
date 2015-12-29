from . import admin

from flask import render_template, url_for, request, redirect, flash
from flask.ext.login import current_user
from .. import db
from ..forms import EditProblemForm, EditContestForm
from ..models import Problem, Contest, User

from datetime import datetime

@admin.route('/edit_problem', methods=['GET', 'POST'])
@admin.route('/edit_problem/<int:pid>', methods=['GET', 'POST'])
@admin.route('/edit_contest/<int:cid>/problem', methods=['GET', 'POST'])
@admin.route('/edit_contest/<int:cid>/problem/<int:pid>', methods=['GET', 'POST'])
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
        if cid == 0:
            return redirect(url_for('oj.list_problems'))
        else:
            contest.problems.append(prob)
            return redirect(url_for('admin.edit_contest', cid=cid))
    return render_template('edit_problem.html', form=form, pid=pid, cid=cid)

@admin.route('/delete_problem/<int:pid>')
def delete_problem(pid = 0):
    problem = Problem.query.get(pid)
    if not problem:
        flash('Contest (pid = %d) not found.' % pid)
        return redirect('/')
    db.session.delete(problem)
    db.session.commit()
    flash('Edit delete successful.')
    return redirect(url_for('oj.list_problems'))

@admin.route('/edit_contest', methods=['GET', 'POST'])
@admin.route('/edit_contest/<int:cid>', methods=['GET', 'POST'])
def edit_contest(cid = 0):
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
        problist = contest.problems
    else:
        contest = Contest()
    form = EditContestForm(obj = contest)
    if form.validate_on_submit():
        form.populate_obj(contest)
        contest.owner = current_user
        db.session.add(contest)
        db.session.commit()
        flash('Edit contest successful.')
        return redirect(url_for('oj.list_contests'))
    return render_template('edit_contest.html', form=form, cid=cid, \
            problems=None if cid == 0 else problist)

@admin.route('/delete_contest/<int:cid>')
def delete_contest(cid = 0):
    contest = Contest.query.get(cid)
    if not contest:
        flash('Contest (cid = %d) not found.' % cid)
        return redirect('/')
    db.session.delete(contest)
    db.session.commit()
    flash('Edit delete successful.')
    return redirect(url_for('oj.list_contests'))

@admin.route('/users')
@admin.route('/users/<int:page>', methods=['GET', 'POST'])
def list_users(page=1):
    users = User.query.paginate(page=page, per_page=20).items
    return render_template('users.html', users=users)

@admin.route('/delete_user/<int:uid>')
def delete_user(uid):
    user = User.query.filter(User.id == uid).first()
    if not user:
        flash('User (uid = %d) not found.' % uid)
        return redirect('/')
    db.session.delete(user)
    db.session.commit()
    flash('Edit problem successful')
    return redirect(url_for(admin.users))

