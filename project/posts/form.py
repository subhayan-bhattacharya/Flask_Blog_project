from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,TextAreaField,BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired,length,EqualTo,ValidationError

class PostForm(FlaskForm):
    title = StringField('Title',validators=[InputRequired(),length(max=40)])
    body = TextAreaField('Body',validators=[InputRequired()])
    new_tag = StringField('New tags')

    def validate_new_tag(form,field):
        data = field.data
        if len(data.split(' ')) > 1:
            raise ValidationError("Please add a comma separated list of single word tags")