from . import oj

from flask import render_template, url_for, request, redirect, flash, abort
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

