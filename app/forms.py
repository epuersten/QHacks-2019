from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.models import NetUser





#######################
# APP FORMS
#######################
class EditSegmentForm(FlaskForm):
    segment_name            = TextAreaField('Segment Name', validators=[Length(min=0, max=140)])
    age_range               = TextAreaField('age range', validators=[Length(min=0, max=140)])
    gender_percent_male     = StringField('gender_percent male', validators=[Length(min=0, max=140)])
    gender_percent_female   = StringField('gender_percent_female', validators=[Length(min=0, max=140)])

    geographic_location     = StringField('geographic location', validators=[Length(min=0, max=140)])

    spear_s                 = StringField('spear_s', validators=[Length(min=0, max=140)])
    spear_p                 = StringField('spear_p', validators=[Length(min=0, max=140)])

    submit                  = SubmitField('Update')



class EditPersonaForm(FlaskForm):
    persona_name            = StringField('Name', validators=[Length(min=0, max=140)])
    persona_photo_file      = StringField('Photo', validators=[Length(min=0, max=3)])

    age                     = StringField('Age', validators=[Length(min=0, max=3)])
    gender                  = StringField('Gender', validators=[Length(min=0, max=1)])

    persona_quote           = TextAreaField('Quote', validators=[Length(min=0, max=140)])
    persona_bio             = TextAreaField('Bio', validators=[Length(min=0, max=500)])

    persona_motivator_likes = TextAreaField('Likes', validators=[Length(min=0, max=140)])
    persona_motivator_dislikes = TextAreaField('Dislikes', validators=[Length(min=0, max=140)])
    persona_goals           = TextAreaField('persona_goals', validators=[Length(min=0, max=140)])
    persona_challenges      = TextAreaField('persona_challenges', validators=[Length(min=0, max=140)])
    persona_values          = TextAreaField('persona_values', validators=[Length(min=0, max=140)])
    persona_routines        = TextAreaField('persona_routines', validators=[Length(min=0, max=140)])

    persona_location        = StringField('persona_location', validators=[Length(min=0, max=140)])
    persona_family          = StringField('persona_family', validators=[Length(min=0, max=140)])

    career_job_title        = StringField('Job_title', validators=[Length(min=0, max=140)])
    career_industry         = StringField('career_industry', validators=[Length(min=0, max=140)])
    career_industry_size    = StringField('career_industry_size', validators=[Length(min=0, max=140)])

    edu_highest_degree      = StringField('edu_highest_degree', validators=[Length(min=0, max=140)])
    edu_topic               = StringField('edu_topic', validators=[Length(min=0, max=140)])

    spear_s                 = StringField('Seeker', validators=[Length(min=0, max=3)])
    spear_p                 = StringField('Pragmat', validators=[Length(min=0, max=3)])
    spear_e                 = StringField('Empat', validators=[Length(min=0, max=3)])
    spear_a                 = StringField('Anchor', validators=[Length(min=0, max=3)])
    spear_r                 = StringField('Reactive', validators=[Length(min=0, max=3)])

    submit                  = SubmitField('Update')






#######################
# AUTH
#######################
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = NetUser.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered.')


class EditProfileForm(FlaskForm):
    first_name = TextAreaField('First Name', validators=[Length(min=0, max=140)])
    last_name = TextAreaField('Last Name', validators=[Length(min=0, max=140)])
    new_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send My Password Reset Link')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Request Password Reset')
