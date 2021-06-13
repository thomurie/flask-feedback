from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, Length

class NewUserForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired(), Length(min=8,max = 128)]) 
    email= StringField('Email Address', validators = [Optional(), Email()])
    first_name = StringField("First Name", validators = [Optional()])
    last_name = StringField('Last Name', validators = [Optional()])

class LoginUserForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()]) 

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators = [InputRequired(), Length(min = 0, max = 100)])
    content = StringField("content", validators = [InputRequired()])
