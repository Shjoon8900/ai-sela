from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class RegisterForm(FlaskForm): #فورم الريجستر 
    username = StringField(label='Full Name', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[
                                Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[
                             Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[
                              EqualTo('password'), DataRequired()])
    department = StringField(label='Address', validators=[
                             Length(min=2, max=30), DataRequired()])
    phone = StringField(label='Phone', validators=[
        Length(min=9, max=11), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm): #فورم اللوق ان 
    email_address = StringField(
        label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class AddComplaint(FlaskForm): #فورم الشكاوى 
    username = StringField(label='Full Name', validators=[
                           Length(min=2, max=30), DataRequired()])
    description = StringField(label='Description', validators=[
        Length(min=2, max=200), DataRequired()])

    phone = StringField(label='Phone', validators=[
        Length(min=9, max=11), DataRequired()])
    submit = SubmitField(label='Submit')


class AddSuggestion(FlaskForm):#فورم الاقتراحات 
    username = StringField(label='Full Name', validators=[
                           Length(min=2, max=30), DataRequired()])
    description = StringField(label='Description ', validators=[
        Length(min=2, max=200), DataRequired()])

    phone = StringField(label='Phone', validators=[
        Length(min=9, max=11), DataRequired()])
    submit = SubmitField(label='Submit')


class AddQuery(FlaskForm):#فورم الاستفسارات 
    username = StringField(label='Full Name', validators=[
                           Length(min=2, max=30), DataRequired()])
    description = StringField(label='Description', validators=[
        Length(min=2, max=200), DataRequired()])

    phone = StringField(label='Phone', validators=[
        Length(min=9, max=11), DataRequired()])
    submit = SubmitField(label='Submit')
