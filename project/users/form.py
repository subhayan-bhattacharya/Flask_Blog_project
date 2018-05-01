from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired,length,EqualTo,ValidationError
from project.models.user_model import User

class RegisterForm(FlaskForm):
    fullname = StringField("Full name",validators=[InputRequired(),length(max=50,message="This field cannot be more than 50 characters")])
    email = EmailField('Email',validators=[InputRequired()])
    username = StringField("User name",validators=[InputRequired(),length(min=4,max=10,message="This field can of length in between 4 and 10 characters")])
    password = PasswordField('New password',validators=[InputRequired(),EqualTo('confirm',message="passwords must match")])
    confirm = PasswordField('Repeat password',validators=[InputRequired()])

    def validate_username(form,field):
        username = field.data
        if User.get_user_by_username(username):
            raise ValidationError("Username is already taken")

    def validate_email(form,field):
        email = field.data
        if User.get_user_by_email(email):
            raise ValidationError("Email already belongs to a user")

class LoginForm(FlaskForm):
    username = StringField("User name", validators=[InputRequired(), length(min=4, max=10,
                                                                            message="This field can of length in between 4 and 10 characters")])
    password = PasswordField('New password',
                             validators=[InputRequired(),])