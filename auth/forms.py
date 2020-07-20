from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('password',validators = [Required(),EqualTo('password_confirm',message = 'Password does not match')])
    password_confirm  = PasswordField('Cornfirm password',validators = [Required()])
    submit = SubmitField('Sign Up')