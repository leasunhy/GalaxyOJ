from . import post

from .. import db
from ..models import Post, Notification, Solution, Tutorial
from ..forms import EditNotificationForm, EditTutorialForm, EditSolutionForm
from ..tools import privilege_required, count_page

from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask.ext.login import current_user, login_required


@post.route('/notifications')
@post.route('/notifications/<int:page>')
def notifications(page = 1):
    notifs = Notification.query.paginate(page=page, per_page=20).items
    return render_template('notifications.html', posts=notifs,
                           page=page, page_count=count_page(Notification, 20))


@post.route('/solutions')
@post.route('/solutions/<int:page>')
def solutions(page = 1):
    solutions = Solution.query.paginate(page=page, per_page=20).items
    return render_template('solution_list.html', posts=solutions,
                           page=page, page_count=count_page(Solution, 20))


@post.route('/tutorials')
@post.route('/tutorials/<int:page>')
def tutorials(page = 1):
    tutorials = Tutorial.query.paginate(page=page, per_page=20).items
    return render_template('tutorial_list.html', posts=tutorials,
                           page=page, page_count=count_page(Tutorial, 20))


@post.route('/notification/<int:id>')
def notification(id):
    p = Notification.query.get_or_404(id)
    return render_template('show_post_base.html', post = p)


@post.route('/solution/<int:id>')
def solution(id):
    p = Solution.query.get_or_404(id)
    return render_template('show_post_base.html', post = p)


@post.route('/tutorial/<int:id>')
def tutorial(id):
    p = Tutorial.query.get_or_404(id)
    return render_template('show_post_base.html', post = p)


@post.route('/new_notification', methods=['GET', 'POST'])
@privilege_required(1)
def new_notification():
    return edit_notification(0)


@post.route('/new_tutorial', methods=['GET', 'POST'])
@login_required
def new_tutorial():
    return edit_tutorial(0)


@post.route('/new_solution', methods=['GET', 'POST'])
@login_required
def new_solution():
    return edit_solution(0)


@post.route('/edit_notification/<int:id>', methods=['GET', 'POST'])
@privilege_required(1)
def edit_notification(id=0):
    p = Notification() if id == 0 else Notification.query.get_or_404(id)
    form = EditNotificationForm(obj = p)
    if form.validate_on_submit():
        form.populate_obj(p)
        if not p.owner:
            p.owner = current_user
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('post.notifications'))
    return render_template('edit_notification.html', form=form, pid=id)


@post.route('/edit_tutorial/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tutorial(id=0):
    p = Tutorial() if id == 0 else Tutorial.query.get_or_404(id)
    if id != 0 and not current_user.is_admin and current_user != p.owner:
        abort(401)
    form = EditTutorialForm(obj = p)
    if form.validate_on_submit():
        form.populate_obj(p)
        if not p.owner:
            p.owner = current_user
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('post.tutorials'))
    return render_template('edit_tutorial.html', form=form, pid=id)


@post.route('/edit_solution/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_solution(id=0):
    p = Solution() if id == 0 else Solution.query.get_or_404(id)
    if id != 0 and not current_user.is_admin and current_user != p.owner:
        abort(401)
    form = EditSolutionForm(obj = p)
    if form.validate_on_submit():
        form.populate_obj(p)
        if not p.owner:
            p.owner = current_user
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('post.solutions'))
    return render_template('edit_solution.html', form=form, pid=id)


@post.route('/delete_post/<int:id>')
@privilege_required(1)
def delete_post(id):
    p = Post.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Post successfully deleted.')
    return redirect(url_for('main.index'))


