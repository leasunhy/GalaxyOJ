from flask.ext.wtf import Form
from wtforms import ValidationError
from wtforms.fields import TextField, TextAreaField,\
        BooleanField, SelectField, SubmitField, PasswordField
from wtforms.validators import Required, Email, EqualTo

from .models import User
 
class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    submit = SubmitField('Log In')

    def validate_password(self, field):
        u = User.query.filter_by(login_name=self.username.data).first()
        if u is None or not u.verify_password(field.data):
            raise ValidationError('Username or password is invalid.')

class SubmitCodeForm(Form):
    probID = TextField('ID')
    language = SelectField('Language', choices=[('p', 'Pascal'), ('cpp', 'C++'), ('c', 'C')])
    code = TextAreaField('text')


class UserRegisterForm(Form):
    login_name = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    confirmpwd = PasswordField('Confirm password',
            validators = [Required(), EqualTo('password', message='Passwords must match')])
    email = TextField('Email', validators = [Email()])
    # unimportant parts
    nickname = TextField('nickname', validators = [Required()])
    signature = TextField('signature')
    real_name = TextField('real_name')
    note = TextAreaField('note')

    def validate_login_name(self, field):
        u = User.query.filter_by(User.login_name==field.data).first()
        if u:
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        u = User.query.filter_by(User.email==field.data).first()
        if u:
            raise ValidationError('Email already exists.')

#class CommentForm(Form):
#    nickname = TextField('NickName')
#    email = TextField('email')
#    text = TextAreaField('text')
#
#class PostForm(Form):
#    title = TextField('title', validators = [Required()])
#    shortcut = TextField('shortcut', validators = [Required()])
#    tag = SelectField('tag', choices=[('d', 'Default'),('a', 'ACM'),('r','Research')])
#    text = TextAreaField('text', id="editor_code")

