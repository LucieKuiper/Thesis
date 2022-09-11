from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
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

class XAIQ(FlaskForm):
    xaiq = StringField('XAIQ', validators=[DataRequired()])
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
    ac = StringField('AC', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')


class TIA(FlaskForm):
    tia1 = StringField('TIA1', validators=[DataRequired()])
    tia2 = StringField('TIA2', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')


class PT(FlaskForm):
    pt1 = StringField('PT1', validators=[DataRequired()])
    pt2 = StringField('PT2', validators=[DataRequired()])
    pt3 = StringField('PT3', validators=[DataRequired()])
    submit = SubmitField('Confirm and Continue')