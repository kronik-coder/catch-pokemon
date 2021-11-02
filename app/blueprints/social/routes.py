from .import bp as social
from app.models import User, Post
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, url_for, request

@social.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        body = request.form.get('body')
        new_post = Post(user_id=current_user.id, body=body)
        new_post.save()
    posts = current_user.all_follower_posts()
    return render_template('index.html.j2', posts=posts)

@social.route('/show_users')
@login_required
def show_users():
    users = User.query.all
    return render_template('show_users.html.j2', users=users)

@social.route('/follow/<int:id>')
@login_required
def follow(id):
    user_to_follow = User.query.get(id)
    current_user.follow(user_to_follow)
    flash(f'You are now following {user_to_follow.first_name} {user_to_follow.last_name}', 'success')
    return redirect(url_for('social.show_users'))

@social.route('/unfollow/<int:id>')
@login_required
def unfollow(id):
    user_to_unfollow = User.query.get(id)
    current_user.unfollow(user_to_unfollow)
    flash(f'You unfollowed {user_to_unfollow.first_name} {user_to_unfollow.last_name}', 'warning')
    return redirect(url_for('social.show_users'))
