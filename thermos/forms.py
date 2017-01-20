from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError

from thermos.models import User

class BookmarkForm(Form):
    url = URLField('The URL for your bookmark: ', validators=[DataRequired(), url()])
    description = StringField('Add an optional description: ')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                       message="Tags can only contain letters and numbers")])

    # We're overriding validation method into better version.
    # This method is called with "form.validate_on_submit()"
    def validate(self):
        if not self.url.data.startswith("http://") or self.url.data.startswith("https://"):
            self.url.data = "http://" + self.url.data

        # Check all other validators.
        if not Form.validate(self):
            return False

        # If there's no description data, make URL the description.
        if not self.description.data:
            self.description.data = self.url.data

        # filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        # Need true to let validate know there's nothing worng.
        return True

class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(3,80), Regexp('^[A-Za-z0-9_]{3,}$', message = 'Username consist of numbers, letters and understores.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must patch.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a username with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')