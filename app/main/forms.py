from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Email, URL, Optional
from wtforms.widgets import TextArea


class CommentForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('E-Mail', validators=[Required(), Email()])
    homepage = StringField('Homepage (optional)')
    comment = StringField('Your Message', widget=TextArea(), validators=[Required()])
    submit = SubmitField('Post')
