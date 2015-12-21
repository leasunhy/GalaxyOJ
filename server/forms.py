from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Email
 
class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = TextField('Password', validators = [Required()])

class SubmitCodeForm(Form):
    probID = TextField('ID')
    language = SelectField('Language', choices=[('p', 'Pascal'), ('cpp', 'C++'), ('c', 'C')])
    code = TextAreaField('text')

class UserRegisterForm(Form):
    username = TextField('Username', validators = [Required()])
    password = TextField('Password', validators = [Required()])
    confirmpwd = TextField('Confirm password', validators = [Required()])
    email = TextField('Email', validators = [Email()])
    # unimportant parts
    nickname = TextField('nickname', validators = [Required()])
    signature = TextField('signature')
    real_name = TextField('real_name')
    note = TextAreaField('note')

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

