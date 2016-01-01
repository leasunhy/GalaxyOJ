from flask.ext.wtf import Form
from wtforms import ValidationError
from wtforms.fields import TextField, TextAreaField,\
        BooleanField, SelectField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Required, Email, EqualTo

from .models import User, Problem
from .tools import sanitize

from judge.config import COMPILER_NAME_LIST, COMPILER_CNT

import datetime

class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    submit = SubmitField('Log In')

    def validate_password(self, field):
        u = User.query.filter_by(login_name=self.username.data).first()
        if u is None or not u.verify_password(field.data):
            raise ValidationError('Username or password is invalid.')

class SubmissionForm(Form):
    compiler = SelectField('Compiler', coerce=int, choices=[(-1, 'Pleaes choose language'), *enumerate(COMPILER_NAME_LIST)])
    code = TextAreaField('Code')
    submit = SubmitField('Submit')
    def validate_compiler(self, field):
        if field.data == -1:
            raise ValidationError('Please select language')

class UpdateProfileForm(Form):
    login_name = TextField('Username', validators = [Required()])
    old_password = PasswordField('Old Password', validators = [Required()])
    new_password = PasswordField('New Password')
    confirm_newpwd = PasswordField('Confirm password',
            validators = [EqualTo('new_password', message='Passwords must match')])
    email = TextField('Email', validators = [Email()])
    # unimportant parts
    nickname = TextField('Nickname')
    signature = TextField('Signature')
    real_name = TextField('Real name')
    note = TextAreaField('Note')

    submit = SubmitField('Update')

    def validate_old_password(self, field):
        u = User.query.filter_by(login_name=self.login_name.data).first()
        if u is None or not u.verify_password(field.data):
            raise ValidationError('Password is invalid.')

class EditUserProfile(Form):
    login_name = TextField('Username', validators = [Required()])
    password = PasswordField('Password')
    email = TextField('Email', validators = [Email()])
    nickname = TextField('Nickname')
    signature = TextField('Signature')
    real_name = TextField('Real name')
    note = TextAreaField('Note')
    submit = SubmitField('Edit')

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
    problem_desc = TextAreaField('Description', filters=[sanitize])
    input_desc = TextAreaField('Input Format', filters=[sanitize])
    output_desc = TextAreaField('Output Format', filters=[sanitize])
    sample_input = TextAreaField('Sample Input', filters=[sanitize])
    sample_output = TextAreaField('Sample Output', filters=[sanitize])
    source = TextField('Source')
    time_limit = TextField('Time Limit', validators = [Required()])
    memory_limit = TextField('Memory Limit', validators = [Required()])
    submit = SubmitField('Submit')

class EditContestForm(Form):
    title = TextField('Title', validators = [Required()])
    description = TextAreaField('Description')
    start_time = TextField('Start time', validators=[Required()])
    end_time = TextField('End time', validators = [Required()])
    password = TextField('Password')
    submit = SubmitField('Submit')

    def validate_end_time(self, field):
        if start_time > end_time:
            raise ValidationError('End time should after start_time')

class EditPostForm(Form):
    title = TextField('Title', validators = [Required()])
    content = TextAreaField('Content', validators=[Required()], filters=[sanitize])
    submit = SubmitField('Submit')


class EditNotificationForm(EditPostForm):
    importance = IntegerField('Importance')


class EditTutorialForm(EditPostForm):
    pass


class EditSolutionForm(EditPostForm):
    problem_id = IntegerField('Problem ID', validators=[Required()])

    def validate_problem_id(self, field):
        if not field.data or not Problem.query.get(field.data):
            raise ValidationError('No such problem.')


class EnterContestForm(Form):
    passcode = PasswordField('Contest Password', validators=[Required()])
    submit = SubmitField('Submit')

