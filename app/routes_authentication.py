######################
# AUTHENTICATION ROUTES
######################
from flask import Flask, render_template, request, redirect, url_for, flash, abort

from app import app, db
# ResetPasswordRequestForm, ResetPasswordForm
from app.forms import LoginForm, RegistrationForm, EditProfileForm
# from app.email import send_email_password_reset
from app.models import NetUser

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os
from datetime import datetime


@login_required
@app.route('/index',  methods=['GET', 'POST'])
def index():
    html = {}
    html['title'] = "Welcome back - Login"
    html['description'] = "Welcome back. Nice to see you."
    html['content'] = "LoggedIn"
    return render_template('user.html', html=html)


##############################
# PUBLIC
##############################
# registration page
@app.route('/register', methods=['GET', 'POST'])
def register():

    html = {}
    html['title'] = "Register"
    html['description'] = "Join us today"
    html['content'] = ""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = NetUser(email=form.email.data, first_name=form.first_name.data,
                       last_name=form.last_name.data, program_name=form.program.data, school_name=form.school.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('register_new.html',
                           html=html,
                           form=form)

# route for login
@app.route('/', methods=['GET', 'POST'])
def login():

    html = {}
    html['title'] = "Welcome back - Login"
    html['description'] = "Welcome back. Nice to see you."
    html['content'] = ""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = NetUser.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',
                           html=html,
                           form=form)

# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# edit user profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    html = {}
    html['title'] = "My Profile"
    html['description'] = ""
    html['content'] = ""

    # Get user profile and record
    user_id = NetUser.user_id
    user = NetUser.query.filter_by(user_id=user_id).first_or_404()

    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.new_email.data
        current_user.date_updated = datetime.utcnow()
        db.session.commit()
        flash('Your profile is updated.', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.new_email.data = current_user.email

    return render_template('editUser.html',
                           html=html,
                           form=form,
                           user=user)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
