from flask import render_template, url_for, redirect, request, Blueprint, flash
from application import load_data, db
from flask_login import login_user, current_user, login_required
from application.main.models import User, PilotUser
from application.main.forms import LoginForm, ShortForm
from random import randint


pilot = Blueprint('pilot', __name__, url_prefix='/dke')
questions_list = load_data()  # CSV list with data
question0 = [0, 29, 28, 32, 1, 15, 5, 16, 24, 8, 4, 10, 22, 7, 18, 30, 6, 26, 31, 27, 3, 20, 12, 11, 17, 2, 25, 19, 21, 14, 13, 23, 9]
question1 = [12, 21, 11, 32, 5, 10, 9, 19, 24, 3, 2, 14, 29, 23, 18, 7, 17, 26, 15, 20, 4, 8, 22, 28, 1, 31, 25, 13, 6, 0, 30, 16, 27]
question2 = [7, 19, 17, 32, 29, 0, 13, 30, 10, 8, 23, 2, 21, 16, 18, 20, 4, 15, 27, 12, 24, 26, 1, 28, 31, 6, 25, 9, 22, 5, 14, 11, 3]
question3 = [10, 27, 11, 32, 7, 29, 1, 16, 6, 19, 26, 13, 28, 14, 18, 20, 31, 5, 21, 2, 8, 9, 0, 12, 23, 4, 25, 3, 15, 24, 17, 30, 22]
question4 = [22, 21, 10, 32, 26,  17, 24, 29, 12, 1, 7, 20, 14, 16, 18, 23, 6, 30, 5, 31, 19, 4, 0, 27, 11, 15, 25, 3, 28, 2, 13, 8, 9]
question_order_list = [question0, question1, question2, question3, question4]


# Route to create user from userID given by prolific and continues to next page
@pilot.route("/", methods=['GET', 'POST'])
def start():
    username = request.args.get('PROLIFIC_PID')
    exsits = User.query.filter_by(username=username).first()
    # Check if new account and needs to be created otherwise show that already done survey
    if exsits is None:
        user = User(username=username, pilot_started=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        order = randint(0, 4)
        pilot_user = PilotUser(username=username, pilot_user=current_user, question_order=order)
        db.session.add(pilot_user)
        db.session.commit()
        return redirect(url_for('pilot.introduction'))
    else:
        user = User.query.filter_by(username=username).first()
        login_user(user)
        if user.pilot_done:
            return redirect(url_for('pilot.done'))
        else:
            if user.pilot_started:
                return redirect(url_for('pilot.go_on'))
            else:
                current_user.pilot_started = True
                pilot_user = PilotUser(username=username, pilot_user=current_user)
                db.session.add(pilot_user)
                db.session.commit()
                return redirect(url_for('pilot.introduction'))


# Page for users that have done survey already
@pilot.route("/done")
def done():
    return render_template('done.html')


# Introduction with information
@pilot.route("/introduction", methods=['GET', 'POST'])
@login_required
def introduction():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('pilot.questions'))
    return render_template('introduction.html', form=form)


# Route to iterate over all questions
@pilot.route("//questions", methods=['POST', 'GET'])
@login_required
def questions():
    form = ShortForm()
    user = PilotUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    order = question_order_list[user.question_order]
    # Check if two attention checks have been answered incorrectly
    if (counter > 14) and (counter < 28):
        wrong_answers = 0
        if user.question32 != 'C':
            wrong_answers += 1
        if user.question18 != 'B':
            wrong_answers += 1
        if (counter > 26) and (user.question25 != 'D'):
            wrong_answers += 1
        if wrong_answers >= 2:
            return redirect("https://app.prolific.co/submissions/complete?cc=C11VJG1L")
    if counter > 32:
        current_user.pilot_done = True
        db.session.commit()
        return redirect("https://app.prolific.co/submissions/complete?cc=CN9BV0IT")
    # Load in questions from data set
    data_context = questions_list.iloc[order[counter]][0]
    data_question = questions_list.iloc[order[counter]][1]
    data_answer0 = questions_list.iloc[order[counter]][2]
    data_answer1 = questions_list.iloc[order[counter]][3]
    data_answer2 = questions_list.iloc[order[counter]][4]
    data_answer3 = questions_list.iloc[order[counter]][5]

    # Check if question has been answered and store answer
    if form.validate_on_submit() and (form.answer.data == 'A' or form.answer.data == 'B' or form.answer.data == 'C'
                                      or form.answer.data == 'D'):
        setattr(user, "question{}".format(order[counter]), form.answer.data)
        user.task_counter = counter + 1
        db.session.commit()
        return redirect(url_for('pilot.questions'))
    # Gives warning when form is submitted with no answer in place
    if request.method == 'POST':
        flash('No answer found, please select an answer', 'danger')

    return render_template('questions.html', form=form, context=data_context, question=data_question, answer0=data_answer0,
                           answer1=data_answer1, answer2=data_answer2, answer3=data_answer3, counter=counter, list=list)


# Login for users that previously left
@pilot.route("/continue", methods=['GET', 'POST'])
@login_required
def go_on():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('pilot.questions'))
    return render_template('continue.html', form=form)


# Route final page that shows user the survey is done
@pilot.route("/end", methods=['GET', 'POST'])
def final():
    return render_template('final.html')
