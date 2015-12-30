from . import oj

import os
from flask import render_template, url_for, request, redirect, flash, abort
from flask.ext.login import login_required, current_user
from .. import app, db, q
from ..forms import SubmissionForm
from ..models import Problem, Contest, Submission

from .. import judge

from judge.config import COMPILER_FILEEXT_LIST

@oj.route('/problems')
@oj.route('/problems/<int:page>')
def list_problems(page = 1):
    problems = Problem.query.filter(Problem.visible==True)\
                    .order_by(Problem.id).paginate(page=page, per_page=20).items
    return render_template('problems.html', problems=problems, admin=True)

@oj.route('/contests')
@oj.route('/contests/<int:page>')
def list_contests(page = 1):
    contests = Contest.query.paginate(page=page, per_page=20).items
    return render_template('contests.html', contests=contests, admin=True)


@oj.route('/status')
@oj.route('/status/<int:page>')
def list_status(page = 1):
    submissions = Submission.query.order_by(Submission.id.desc())\
                                  .paginate(page=page, per_page=20).items
    return render_template('status.html', submissions=submissions)

def sum_up_verdicts(verdicts):
    if verdicts is None or verdicts == []:
        return ''
    if 'Accepted' in verdicts:
        return 'Accepted'
    return 'Stucked%d'%len(verdicts)

def count_ac(summary):
    return sum([verdict == 'Accepted' for verdict in summary])

@oj.route('/contest/<int:id>')
def contest(id = 1):
    contest = Contest.query.get_or_404(id)
    users = db.session.query(distinct(User.name)).filter(Submission.contest==contest)
    for u in users:
        verdict_list = []
        q = db.session.query(sum_up_verdicts(Submission.verdict))\
                .filter(Submission.contest==contest and User.id == u.id)\
                .group_by(Problem)
        res = list(q)
        verdict_list.append(res)
        all_ac.append(count_ac(res))
    return render_template('show_contest.html', c=contest)

@oj.route('/problem/<int:pid>')
@oj.route('/contest/<int:cid>/problems/<int:pid>')
def problem(cid = 0, pid = 1):
    if cid == 0:
        problem = Problem.query.get_or_404(pid)
    else:
        contest = Contest.query.get_or_404(cid)
        try:
            problem = contest.problems[pid-1]
        except IndexError:
            abort(404)
    return render_template('show_problem.html', p=problem, cid=cid, pid=pid)

def save_to_file(data, submit):
    filename = os.path.join(app.config['SUBMISSION_FOLDER'], str(submit.id) + COMPILER_FILEEXT_LIST[submit.compiler_id])
    file = open(filename, 'w')
    file.write(data)
    file.close()
    return filename

def send_to_judge(submit, problem):
    sid = submit.id
    source_path = submit.filename
    testcase_folder = os.path.join(app.config['TESTCASE_FOLDER'], str(problem.id))
    compiler_id = submit.compiler_id
    time_limit = problem.time_limit
    memory_limit = problem.memory_limit
    job = q.enqueue_call(
            func = judge,
            args = (sid, source_path, testcase_folder,
                compiler_id, time_limit, memory_limit),
            result_ttl = 5000)

@oj.route('/submit/<int:pid>', methods = ['GET', 'POST'])
@oj.route('/contest/<int:cid>/submit/<int:pid>', methods = ['GET', 'POST'])
@login_required
def submit_code(cid = 0, pid = 1):
    if cid == 0:
        problem = Problem.query.get_or_404(pid)
    else:
        contest = Contest.query.get_or_404(cid)
        try:
            problem = contest.problems[pid-1]
        except IndexError:
            abort(404)
    form = SubmissionForm()
    if form.validate_on_submit():
        submit = Submission()
        submit.owner = current_user
        submit.problem = problem
        submit.compiler_id = form.compiler.data
        submit.code_length = len(form.code.data)
        db.session.add(submit)
        db.session.commit()
        submit.filename = save_to_file(form.code.data, submit)
        send_to_judge(submit, problem)
        return redirect('oj/status')
    return render_template('submit_code.html', form = form, cid = cid, pid = pid,
            problem = problem)

