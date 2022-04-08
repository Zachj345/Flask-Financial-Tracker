from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('woah there! that usernames already taken', category='error')
        elif len(username) < 2:
            flash('username must be longer than 1 character', category='error')
        elif len(password1) < 4:
            flash('password should be at least 4 characters', category='error')
        elif password1 != password2:
            flash('passwords must match', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('account successfully created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password!', category='error')
        else:
            flash('username non-existent', category='error')
    return render_template('log_in.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
