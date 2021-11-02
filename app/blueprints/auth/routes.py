from flask import render_template, request, redirect, url_for, flash
from wtforms.validators import Email
from .forms import EditProfileForm, LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from .import bp as auth

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            error_string = 'So there was an error, you might wanna try again, idk'
            return render_template('registration.html.j2', error=error_string, form=form)

        return redirect(url_for('auth.login'))

    return render_template('registration.html.j2', form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('You are logged in', 'success')
            return redirect(url_for('social.index'))
        error_string = 'So there was an error with your email/password. You might wanna try again, idk'
        return render_template('registration.html.j2', error=error_string, form=form)
    return render_template('login.html.j2', form=form)

@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data
        }
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash('Email already in use bruh', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile updated!', 'success')
        except:
            flash('There was an unexpexted error', 'danger')
            return redirect(url_for('auth.edit_profile'))
    return render_template('registration.html.j2', form=form)