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
    compiler = SelectField('Compiler', coerce=int, choices=[(-1, 'Pleaes choose language'), *enumerate(COMPILER_NAME_LIST)])
    code = TextAreaField('Code')
    submit = SubmitField('Submit')
    def validate_compiler(self, field):
        if field.data == -1:
            raise ValidationError('Please select language')

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

class EditContestForm(Form):
    title = TextField('Title', validators = [Required()])
    description = TextAreaField('Description')
    start_time = TextField('Start time')
    end_time = TextField('End time')
    password = TextField('Password')
    submit = SubmitField('Submit')
