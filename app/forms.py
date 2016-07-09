from flask_wtf import Form 
from wtforms import BooleanField, TextField, PasswordField, validators
from wtforms.validators import Length, Required, EqualTo
from flask_wtf.html5 import EmailField


class RegistrationForm(Form):
    username = TextField('Username', [Length(min=4, max=25),Required()])
    email = TextField('Email Address', [Length(min=6, max=35),Required()])
    avatar = TextField("Avatar")
    password = PasswordField('New Password', [
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [Required()])

class LoginForm(Form):
    email = EmailField("Email Address", [Required()])
    password = PasswordField("Password", [Required()])
    