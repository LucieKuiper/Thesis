from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired


# Stores answer in survey
class ShortForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    confidence = RadioField('Are you confident about your answer?', choices=[('yes','Confident about answer'),('no', 'NOT confident about answer')])
    submit = SubmitField('Confirm and Continue')


class OtherForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')


class LoginForm(FlaskForm):
    submit = SubmitField('Confirm and Continue')
