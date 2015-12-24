from flask.ext.wtf import Form
from wtforms import ValidationError
from wtforms.fields import TextField, TextAreaField,\
        BooleanField, SelectField, SubmitField, PasswordField
from wtforms.validators import Required, Email, EqualTo

from .models import User

from judge.config import COMPILER_NAME_LIST, COMPILER_CNT
 
class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    submit = SubmitField('Log In')

    def validate_password(self, field):
        u = User.query.filter_by(login_name=self.username.data).first()
        if u is None or not u.verify_password(field.data):
            raise ValidationError('Username or password is invalid.')

class SubmissionForm(Form):
    problem_id = TextField('ID')
    language = SelectField('Compiler', choices=[(0, 'Pleaes choose language'), *[(i + 1, COMPILER_NAME_LIST[i]) for i in range(COMPILER_CNT)]])
    code = TextAreaField('Code')
    submit = SubmitField('Submit')


class UserRegisterForm(Form):
    login_name = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    confirmpwd = PasswordField('Confirm password',
            validators = [Required(), EqualTo('password', message='Passwords must match')])
    email = TextField('Email', validators = [Email()])
    # unimportant parts
    nickname = TextField('Nickname')
    signature = TextField('Signature')
    real_name = TextField('Real name')
    note = TextAreaField('Note')

    submit = SubmitField('Register')

    def validate_login_name(self, field):
        u = User.query.filter(User.login_name==field.data).first()
        if u:
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        u = User.query.filter(User.email==field.data).first()
        if u:
            raise ValidationError('Email already exists.')

class EditProblemForm(Form):
    title = TextField('Title', validators = [Required()])
    problem_desc = TextAreaField('Description')
    input_desc = TextAreaField('Input Format')
    output_desc = TextAreaField('Output Format')
    sample_input = TextAreaField('Sample Input')
    sample_output = TextAreaField('Sample Output')
    source = TextField('Source')
    time_limit = TextField('Time Limit', validators = [Required()])
    memory_limit = TextField('Memory Limit', validators = [Required()])
    submit = SubmitField('Submit')

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

