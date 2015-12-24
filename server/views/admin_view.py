from . import admin

from flask import render_template, url_for, request, redirect, flash
from .. import db
from ..forms import EditProblemForm
from ..models import Problem, Contest

@admin.route('/edit_problem/<int:pid>', methods=['GET', 'POST'])
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
        return redirect(url_for('oj.list_problems'))
    return render_template('edit_problem.html', form=form, pid=pid, cid=cid)

