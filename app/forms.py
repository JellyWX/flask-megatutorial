from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if len(username) > 32:
            raise ValidationError('Please enter a username less than 32 characters')

        user = User.query.filter_by(username=username.data).first()

        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError('Email already in use')


class PostForm(FlaskForm):
    body = StringField('Make a new post:', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_body(self, body):
        if len(body) > 140:
            raise ValidationError('Must be shorter than 140 characters (you used {})'.format(len(body)))
