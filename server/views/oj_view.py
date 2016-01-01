from . import oj

import os
import datetime
from flask import render_template, url_for, request, redirect, flash, abort, session
from flask.ext.login import login_required, current_user
from .. import app, db, q

from ..forms import SubmissionForm, EnterContestForm
from ..models import Problem, Contest, Submission, User, Standing

from .. import judge

from judge.config import COMPILER_FILEEXT_LIST


def check_enterable(contest):
    if contest.passcode_hash and\
            (contest.id not in session.setdefault('contests', [])):
        return False
    return True


@oj.route('/problems')
@oj.route('/problems/<int:page>')
def list_problems(page = 1):
    problems = Problem.query.order_by(Problem.id)\
            .paginate(page=page, per_page=20).items
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


@oj.route('/enter_contest/<int:cid>', methods=['GET', 'POST'])
def enter_contest(cid):
    contest = Contest.query.get_or_404(cid)
    if not contest.passcode_hash:
        return redirect(url_for('oj.contest', id = cid))
    form = EnterContestForm()
    if form.validate_on_submit():
        if contest.verify_passcode(form.passcode.data):
            session.setdefault('contests', []).append(contest.id)
            return redirect(url_for('oj.contest', id=contest.id))
        else:
            form.errors.setdefault('passcode', []).append('Passcode incorrect.')
    return render_template('enter_contest.html', form = form, contest = contest)


@oj.route('/contest/<int:id>')
def contest(id = 1):
    contest = Contest.query.get_or_404(id)
    if not check_enterable(contest):
        return redirect(url_for('oj.enter_contest', cid=contest.id))
    from sqlalchemy import distinct
    users = list(db.session.query(distinct(Standing.user_id))\
            .filter(Standing.contest_id==contest.id))
    standing = []
    for u in users:
        verdicts = []
        for p in contest.problems:
            q = db.session.query(Standing.actime, Standing.penalty, Standing.submissions)\
                    .filter(Standing.contest_id==contest.id)\
                    .filter(Standing.problem_id==p.id)\
                    .filter(Standing.user_id == u[0])
            result = list(q)
            verdicts.extend(result)
        ac_num = sum(bool(u[0]) for u in verdicts)
        penalty = sum(u[1] for u in verdicts)
        standing.append((User.query.get(u[0]), ac_num, penalty, verdicts))
    standing.sort(key = lambda u:(u[1],u[2]), reverse=True)
    print(standing)
    return render_template('show_contest.html', c=contest, standing=standing)


@oj.route('/problem/<int:pid>')
@oj.route('/contest/<int:cid>/problems/<int:pid>')
def problem(cid = 0, pid = 1):
    if cid == 0:
        problem = Problem.query.get_or_404(pid)
    else:
        contest = Contest.query.get_or_404(cid)
        if not check_enterable(contest):
            return redirect(url_for('oj.enter_contest', cid=contest.id))
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
    db.session.query(Submission).filter(Submission.id==sid).update(verdict)
    db.session.commit()
    s = Submission.query.get(sid)
    if s.contest_id:
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
        _delta = datetime.datetime.now() - contest.start_time
        rc.add_record(verdict['verdict'], _delta)
        db.session.add(rc)
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



@oj.route('/contest/<int:cid>/submit/<int:pid>', methods = ['GET', 'POST'])
@login_required
def contest_submit_code(cid, pid):
    return submit_code(cid=cid, pid=pid)


@oj.route('/submit/<int:pid>', methods = ['GET', 'POST'])
@login_required
def submit_code(pid, cid=0):
    if cid == 0:
        problem = Problem.query.get_or_404(pid)
    else:
        contest = Contest.query.get_or_404(cid)
        if not check_enterable(contest):
            return redirect(url_for('oj.enter_contest', cid=contest.id))
        try:
            problem = contest.problems[pid-1]
        except IndexError:
            abort(404)
    form = SubmissionForm()
    if form.validate_on_submit():
        submit = Submission()
        submit.owner = current_user
        submit.problem = problem
        if cid != 0: submit.contest_id = cid
        submit.compiler_id = form.compiler.data
        submit.code_length = len(form.code.data)
        db.session.add(submit)
        db.session.commit()
        submit.filename = save_to_file(form.code.data, submit)
        send_to_judge(submit, problem)
        return redirect(url_for('oj.list_status'))
    return render_template('submit_code.html', form = form, cid = cid, pid = pid,
            contest = contest if cid else None,
            problem = problem)

