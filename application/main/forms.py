from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, TextField, IntegerField
from wtforms.validators import DataRequired


# Stores answer in survey
class ShortForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    confidence = RadioField('Are you confident about your answer?',
                            choices=[('yes', 'Confident about answer'), ('no', 'NOT confident about answer')])
    submit = SubmitField('Confirm and Continue')


class OtherForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')


class LoginForm(FlaskForm):
    submit = SubmitField('Confirm and Continue')


class Survey(FlaskForm):
    self = StringField('Self', validators=[DataRequired()])
    other = StringField('Other', validators=[DataRequired()])
    percentage = IntegerField('Percentage', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')
