from . import admin

from flask import render_template, url_for, request, redirect, flash, abort
from flask.ext.login import current_user, login_required
from .. import app, db
from ..forms import EditProblemForm, EditContestForm, EditUserProfile, ManageUserProfile
from ..models import Problem, Contest, User

from werkzeug import secure_filename
from werkzeug.security import safe_join

from datetime import datetime
from ..tools import privilege_required, root_required, ROOT_PRIVILEGE

import os


@admin.route('/new_problem', methods=['GET', 'POST'])
@privilege_required(1)
def new_problem():
    return edit_problem(pid=0)


@admin.route('/new_contest_problem/<int:cid>', methods=['GET', 'POST'])
@privilege_required(1)
def new_contest_problem(cid):
    return edit_contest_problem(cid=cid, pid=0)


@admin.route('/edit_contest/<int:cid>/problem/<int:pid>', methods=['GET', 'POST'])
@privilege_required(1)
def edit_contest_problem(cid, pid):
    contest = Contest.query.get_or_404(cid)
    try:
        prob = Problem() if pid == 0 else contest.problems[pid-1]
    except IndexError:
        abort(404)
    form = EditProblemForm(obj=prob)
    if form.validate_on_submit():
        form.populate_obj(prob)
        prob.visible = prob.visible or contest.end_time < datetime.now()
        contest.problems.append(prob)
        db.session.add(prob)
        db.session.add(contest)
        db.session.commit()
        flash('Edit problem successful.')
        return redirect(url_for('admin.edit_contest', cid=cid))
    if form.errors:
        for f, e in form.errors.items():
            flash("%s: %s" % (f, e))
    return render_template('edit_problem.html', form=form, pid=pid)


@admin.route('/edit_problem/<int:pid>', methods=['GET', 'POST'])
@privilege_required(1)
def edit_problem(pid=0):
    prob = Problem() if pid == 0 else Problem.query.get_or_404(pid)
    prob.visible = True
    form = EditProblemForm(obj=prob)
    if form.validate_on_submit():
        form.populate_obj(prob)
        db.session.add(prob)
        db.session.commit()
        flash('Edit problem successful.')
        return redirect(url_for('oj.list_problems'))
    return render_template('edit_problem.html', form=form, pid=pid)


@admin.route('/toggle_problem_state/<int:pid>', methods=['POST'])
@privilege_required(1)
def toggle_problem_state(pid):
    prob = Problem.query.get_or_404(pid)
    prob.visible = not prob.visible
    db.session.add(prob)
    db.session.commit()
    return 'success'


@admin.route('/delete_problem/<int:pid>')
@privilege_required(1)
def delete_problem(pid=0):
    problem = Problem.query.get(pid)
    if not problem:
        flash('Contest (pid = %d) not found.' % pid)
        return redirect('/')
    db.session.delete(problem)
    db.session.commit()
    flash('Edit delete successful.')
    return redirect(url_for('oj.list_problems'))


@admin.route('/new_contest', methods=['GET', 'POST'])
@privilege_required(1)
def new_contest():
    return edit_contest(cid=0)


@admin.route('/edit_contest/<int:cid>', methods=['GET', 'POST'])
@privilege_required(1)
def edit_contest(cid=0):
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
    return render_template('edit_contest.html', form=form, cid=cid,
                           problems=[] if cid == 0 else problist)


@admin.route('/delete_contest/<int:cid>')
@privilege_required(1)
def delete_contest(cid=0):
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
@privilege_required(1)
def list_users(page=1):
    users = User.query.filter(User.privilege_level<=current_user.privilege_level)\
            .order_by(User.id).paginate(page=page, per_page=20).items
    return render_template('users.html', users=users, ROOT_PRIVILEGE=ROOT_PRIVILEGE)


@admin.route('/manage_user/<int:uid>', methods=['GET', 'POST'])
@root_required()
def manage_user(uid):
    user = User.query.get(uid)
    if user is None:
        flash('User <%d> not found' % (uid))
        redirect('/')
    form = ManageUserProfile(obj = user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('Update successful')
        return redirect('/')
    return render_template('manage_user.html', form=form, uid=uid)


@admin.route('/delete_user/<int:uid>')
@privilege_required(1)
def delete_user(uid):
    user = User.query.filter(User.id == uid).first()
    if not user:
        flash('User (uid = %d) not found.' % uid)
        return redirect('/')
    db.session.delete(user)
    db.session.commit()
    flash('Edit problem successful')
    return redirect(url_for('admin.users'))


def is_valid_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['in', 'out'])


@admin.route('/manage_data/<int:pid>', methods=['GET', 'POST'])
@privilege_required(1)
def manage_data(pid):
    datadir = os.path.join(app.config['TESTCASE_FOLDER'], str(pid))
    print(request.method)
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file in files:
            if is_valid_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(datadir): os.makedirs(datadir)
                file.save(os.path.join(datadir, filename))
        return redirect(url_for('admin.manage_data', pid=pid))
    import glob
    infiles = glob.glob(os.path.join(datadir, "*.in"))
    infiles.sort()
    outfiles = glob.glob(os.path.join(datadir, "*.out"))
    outfiles.sort()
    fun = lambda st : st[len(datadir) + 1 :]
    return render_template('upload_data.html', pid=pid,
                           infiles=map(fun, infiles),
                           outfiles=map(fun, outfiles))


@admin.route('/delete_testcase/<int:pid>/<fname>')
@privilege_required(1)
def delete_testcase(pid, fname):
    datadir = os.path.join(app.config['TESTCASE_FOLDER'], str(pid))
    filename = safe_join(datadir, fname)
    if os.path.exists(filename):
        os.remove(filename)
    return redirect(url_for('admin.manage_data', pid=pid))


@admin.route('/edit_user/<int:uid>', methods=['GET', 'POST'])
def edit_user(uid):
    user = User.query.get(uid)
    if user is None:
        flash('User <%d> not found' % (uid))
        redirect('/')
    form = EditUserProfile(obj = user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('Update successful')
        return redirect('/')
    return render_template('edit_user.html', form=form, uid=uid)

