from . import oj

from flask import render_template, url_for, request, redirect, flash, abort
from flask.ext.login import login_required, current_user
from .. import db
from ..forms import SubmissionForm
from ..models import Problem, Contest, Submission

@oj.route('/problems')
@oj.route('/problems/<int:page>')
def list_problems(page = 1):
    problems = Problem.query.filter(Problem.visible==True)\
                    .order_by(Problem.id).paginate(page=page, per_page=20).items
    return render_template('problems.html', problems=problems)


@oj.route('/contests')
@oj.route('/contests/<int:page>')
def list_contests(page = 1):
    contests = Contest.query.paginate(page=page, per_page=20).items
    return render_template('contests.html', contests=contests)


@oj.route('/status')
@oj.route('/status/<int:page>')
def list_status(page = 1):
    submissions = Submission.query.order_by(Submission.id.desc())\
                                  .paginate(page=page, per_page=20).items
    return render_template('status.html', submissions=submissions)


@oj.route('/contest/<int:id>')
def contest(id = 1):
    contest = Contest.query.get_or_404(id)
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
    return render_template('show_problem.html', p=problem)

def save_to_file(data, submission_id)
    f = open(file_name, 'w')
    f.write(data)
    f.close()

@login_required
@oj.route('/submit/<int:pid>', methods = ['GET', 'POST'])
@oj.route('/contest/<int:cid>/submit/<int:pid>', methods = ['GET', 'POST'])
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
        db.session.add(submit)
        db.session.commit()
        save_to_file(form.code.data, submit.id)
        return "haha"
    print("Invalid")
    return render_template('submit_code.html', form = form, cid = cid, pid = pid)
