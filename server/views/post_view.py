from flask import render_template, url_for, request, redirect, flash, jsonify, session

from . import post
from ..models import Post, Notification, Solution, Tutorial

@post.route('/notifications')
@post.route('/notifications/<int:page>')
def notifications(page = 1):
    notifs = Notification.query.paginate(page=page, per_page=20).items
    return render_template('index.html', posts=notifs)


@post.route('/solutions')
@post.route('/solutions/<int:page>')
def solutions(page = 1):
    solutions = Solution.query.paginate(page=page, per_page=20).items
    return render_template('solution_list.html', posts=solutions)


@post.route('/tutorials')
@post.route('/tutorials/<int:page>')
def tutorials(page = 1):
    tutorials = Tutorial.query.paginate(page=page, per_page=20).items
    return render_template('tutorial_list.html', posts=tutorials)


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


