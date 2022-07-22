from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


# Stores answer in survey
class ShortForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')

class LoginForm(FlaskForm):
    submit = SubmitField('Confirm and Continue')
