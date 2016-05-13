from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required, URL


class LoginForm(Form):
    name = StringField('Admin name:', validators=[Required()])
    password = PasswordField('Password:', validators=[Required()])
    submit = SubmitField('Login')


class NewPostForm(Form):
    title = StringField('Title', validators=[Required()])
    formatted_title = StringField('Formatted Title')
    subtitle = StringField('Subtitle')
    tags = StringField('Tags')
    content = PageDownField('Content', validators=[Required()])
    image_url = StringField('Image URL', validators=[URL()])
    submit = SubmitField('Post')

