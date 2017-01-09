from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(Form):
    url = URLField('The URL for your bookmark: ', validators=[DataRequired(), url()])
    description = StringField('Add an optional description: ')

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

        # Need true to let validate know there's nothing worng.
        return True

