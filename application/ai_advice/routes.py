from flask import Blueprint
from flask import render_template, url_for, redirect, request
from application import load_data, db
from flask_login import login_user, current_user, login_required
from application.ai_advice.models import AIUser
from application.main.forms import LoginForm, OtherForm





ai_advice = Blueprint('ai_advice', __name__)
questions_list = load_data("AIadvice.csv")  # CSV list with data


# Route to create user from userID given by prolific and continues to next page
@ai_advice.route("/advice/", methods=['GET', 'POST'])
def start():
    userid = request.args.get('PROLIFIC_PID')
    exsits = AIUser.query.filter_by(userid=userid).first()
    # Check if new account and needs to be created otherwise show that already done survey
    if exsits is None:
        user = AIUser(userid=userid)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('ai_advice.introduction'))
    else:
        return redirect(url_for('ai_advice.done'))


# Page for users that have done survey already
@ai_advice.route("/advice/done")
def done():
    return render_template('done.html')


# Introduction with information
@ai_advice.route("/advice/introduction", methods=['GET', 'POST'])
@login_required
def introduction():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('introduction.html', form=form)


# Route to iterate over all questions
@ai_advice.route("/advice/questions", methods=['POST', 'GET'])
@login_required
def questions():
    form = OtherForm()
    counter = current_user.task_counter  # counter that tracks at which question the user is
    if counter > 3:
        return redirect(url_for('ai_advice.final'))
    # Load in questions from data set
    data_context = questions_list.iloc[counter][0]
    data_question = questions_list.iloc[counter][1]
    data_answer0 = questions_list.iloc[counter][2]
    data_answer1 = questions_list.iloc[counter][3]
    data_answer2 = questions_list.iloc[counter][4]
    data_answer3 = questions_list.iloc[counter][5]
    data_advice = questions_list.iloc[counter][7]

    # Check if question has been answered and store answer
    if form.validate_on_submit():
        setattr(current_user, "question{}".format(counter), form.answer.data)
        current_user.task_counter = counter + 1
        db.session.commit()
        return redirect(url_for('ai_advice.questions'))
    return render_template('AIquestions.html', form=form, context=data_context, question=data_question,
                           answer0=data_answer0, answer1=data_answer1, answer2=data_answer2, answer3=data_answer3,
                           counter=counter, list=list, advice=data_advice)


# Route final page that shows user the survey is done
@ai_advice.route("/advice/end", methods=['GET', 'POST'])
def final():
    return render_template('final.html')
