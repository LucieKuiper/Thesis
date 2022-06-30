from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField


# Stores answer in survey
class ShortForm(FlaskForm):
    answer = RadioField(u'Choices', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    submit = SubmitField('Confirm and Continue')


class LoginForm(FlaskForm):
    submit = SubmitField('Confirm and Continue')
