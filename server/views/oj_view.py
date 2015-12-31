from . import oj

import os
from flask import render_template, url_for, request, redirect, flash, abort
from flask.ext.login import login_required, current_user
from .. import app, db, q
from ..forms import SubmissionForm
from ..models import Problem, Contest, Submission, User, Standing

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
    if verdicts is None: return (False, 0)
    isAC = 'Accepted' in map(lambda u:u[1], verdicts)
    return (isAC, len(verdicts))

from sqlalchemy import distinct
@oj.route('/contest/<int:id>')
def contest(id = 1):
    contest = Contest.query.get_or_404(id)
    users = list(db.session.query(distinct(User.id))\
            .filter(Submission.contest_id==contest.id))
    standing = []
    for u in users:
        verdicts = []
        for p in contest.problems:
            q = db.session.query(Submission.problem_id,Submission.verdict)\
                    .filter(Submission.contest_id==contest.id)\
                    .filter(Submission.problem_id==p.id)\
                    .filter(Submission.user_id == u[0])
            result = sum_up_verdicts(list(q))
            verdicts.append(result)
        ac_num = sum(u[0] for u in verdicts)
        standing.append((User.query.get(u[0]), ac_num, verdicts))
    standing.sort(key = lambda u:u[1], reverse=True)
    print(standing)
    return render_template('show_contest.html', c=contest, standing=standing)

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

def save_to_database(job_id):
    job = q.fetch_job(job_id)
    (sid, verdict) = job.result
    s = Submission.query.get(sid).update(verdict)
    if s.contest_id != 0:
        contest = Contest.query.get(s.contest_id)
        rc = Standing.query\
                .filter(Standing.contest_id==s.contest_id)\
                .filter(Standing.problem_id==s.problem_id)\
                .filter(Standing.user_id==s.user_id)\
                .first()
        if rc is None: 
            rc = Standing(
                    contest_id = s.contest_id,
                    problem_id = s.problem_id,
                    user_id = s.user_id,
                )
        _delta = datetime.now() - contest.start_time
        rc.add_record(verdict, _delta)
    db.session.commit()

def send_to_judge(submit, problem):
    sid = submit.id
    source_path = submit.filename
    testcase_folder = os.path.join(app.config['TESTCASE_FOLDER'], str(problem.id))
    compiler_id = submit.compiler_id
    time_limit = problem.time_limit
    memory_limit = problem.memory_limit
    judge_job = q.enqueue_call(
            func = judge,
            args = (sid, source_path, testcase_folder,
                compiler_id, time_limit, memory_limit),
            result_ttl = 5000)
    upd_job = q.enqueue_call(
            func = save_to_database,
            depends_on = judge_job,
            args = (judge_job.id,),
            )

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
        submit.contest_id = cid
        submit.compiler_id = form.compiler.data
        submit.code_length = len(form.code.data)
        db.session.add(submit)
        db.session.commit()
        submit.filename = save_to_file(form.code.data, submit)
        send_to_judge(submit, problem)
        return redirect('oj/status')
    return render_template('submit_code.html', form = form, cid = cid, pid = pid,
            contest = contest if cid else None,
            problem = problem)

