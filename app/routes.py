from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        print(request.args)

    else:
        print(request.form)

    return render_template('test.html', title='Test')

@app.route('/')
@app.route('/index')
@login_required
def index():

    posts = [
    {'author' : {'username' : 'John'},
    'content' : 'REEEEEEEEEEEEEEEE'},

    {'author' : {'username' : 'Jan'},
    'content' : 'edwfrgthyjujfhgfgfnghtergs'},

    {'author' : {'username' : 'Jen'},
    'content' : 'Raaaaaaaaaaaaaaaaaaaaaaa'}
    ]

    return render_template('index.html', title='Home', user=current_user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    else:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))

            else:
                login_user(user, remember=form.remember_me.data)

                next_page = request.args.get('next')

                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)

        else:
            return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash('Thank you for registering, {}'.format(user.username))

            return redirect(url_for('index'))

        else:
            return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
