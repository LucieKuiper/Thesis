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
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')


class ATI(FlaskForm):
    ati1 = StringField('ATI1', validators=[DataRequired()])
    ati2 = StringField('ATI2', validators=[DataRequired()])
    ati3 = StringField('ATI3', validators=[DataRequired()])
    ati4 = StringField('ATI4', validators=[DataRequired()])
    ati5 = StringField('ATI5', validators=[DataRequired()])
    ati6 = StringField('ATI6', validators=[DataRequired()])
    ati7 = StringField('ATI7', validators=[DataRequired()])
    ati8 = StringField('ATI8', validators=[DataRequired()])
    ati9 = StringField('ATI9', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')


class TIA(FlaskForm):
    tia1 = StringField('TIA1', validators=[DataRequired()])
    tia2 = StringField('TIA2', validators=[DataRequired()])
    tia3 = StringField('TIA3', validators=[DataRequired()])
    tia4 = StringField('TIA4', validators=[DataRequired()])
    tia5 = StringField('TIA5', validators=[DataRequired()])

    submit = SubmitField('Confirm and Continue')