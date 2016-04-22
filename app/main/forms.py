from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Email, URL

class CommentForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('E-Mail', validators=[Required(), Email()])
    homepage = StringField('Homepage (optional)', validators=[URL()])
    submit = SubmitField('Post')
