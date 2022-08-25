from flask import render_template, url_for, redirect, request, flash, Blueprint
from application import load_data, db
from flask_login import login_user, current_user, login_required
from application.main.models import User, AIUser
from application.main.forms import LoginForm, OtherForm, Survey
from random import randint

ai_advice = Blueprint('ai_advice', __name__, url_prefix='/ai')
questions_list = load_data("/static/AIadvice.csv")  # CSV list with data

question0 = [1, 4, 5, 2, 3, 0, 6, 7, 11, 10, 8, 9, 14, 17, 13, 18, 12, 16, 15]
question1 = [12, 18, 17, 13, 14, 16, 15, 9, 11, 10, 8, 7, 5, 0, 2, 1, 4, 6, 3]
question2 = [1, 6, 4, 5, 0, 3, 2, 11, 8, 10, 9, 7, 15, 13, 17, 14, 18, 16, 12]
question3 = [12, 18, 16, 17, 14, 13, 15, 10, 8, 9, 11, 7, 2, 4, 5, 0, 6, 3, 1]
question4 = [3, 1, 4, 6, 2, 0, 5, 11, 8, 10, 9, 7, 17, 13, 18, 15, 12, 16, 14]
question5 = [16, 13, 14, 17, 12, 18, 15, 11, 9, 10, 8, 7, 0, 5, 1, 6, 3, 4, 2]
question6 = [4, 1, 3, 0, 2, 6, 5, 8, 11, 7, 10, 9, 17, 16, 13, 18, 15, 14, 12]
question7 = [12, 14, 16, 17, 18, 15, 13, 8, 7, 10, 11, 9, 3, 2, 4, 1, 6, 5, 0]
question8 = [2, 0, 6, 4, 5, 3, 1, 8, 9, 7, 11, 10, 16, 15, 17, 18, 12, 13, 14]
question9 = [12, 14, 16, 15, 13, 17, 18, 10, 9, 11, 8, 7, 0, 4, 6, 5, 3, 2, 1]
question_order_list = [question0, question1, question2, question3, question4, question5, question6, question7,
                       question8, question9]


# Route to create user from userID given by prolific and continues to next page
@ai_advice.route("/", methods=['GET', 'POST'])
def start():
    username = request.args.get('PROLIFIC_PID')
    exsits = User.query.filter_by(username=username).first()
    # Check if new account and needs to be created, and create if needed
    if exsits is None:
        user = User(username=username, ai_started=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        order = randint(0, 9)
        version = randint(0, 1)
        ai_user = AIUser(username=username, AI_user=current_user, tutorial=version, question_order=order)
        db.session.add(ai_user)
        db.session.commit()
        return redirect(url_for('ai_advice.introduction'))
    # Logs in if account already existent and check whether has done survey already
    else:
        user = User.query.filter_by(username=username).first()
        login_user(user)
        if user.ai_done:
            return redirect(url_for('ai_advice.done'))
        else:
            if user.ai_started:
                return redirect(url_for('ai_advice.go_on'))
            else:
                current_user.ai_started = True
                ai_user = AIUser(username=username, AI_user=current_user)
                db.session.add(ai_user)
                db.session.commit()
                return redirect(url_for('ai_advice.introduction'))


# Page for users that have done survey already
@ai_advice.route("/done")
def done():
    return render_template('done.html')


# Introduction with information
@ai_advice.route("/introduction", methods=['GET', 'POST'])
@login_required
def introduction():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('introductionAI.html', form=form)


# Route to iterate over all questions
@ai_advice.route("/questions", methods=['POST', 'GET'])
@login_required
def questions():
    form = OtherForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is

    if counter > 18:
        current_user.ai_done = True
        db.session.commit()
        return redirect(url_for('ai_advice.survey'))

    question_number = question_order_list[user.question_order][counter]
    old_answer = user.previous

    if counter == 7 and user.previous != 'E':
        user.previous = 'E'
        db.session.commit()
        return redirect(url_for('ai_advice.survey'))

    elif counter == 12 and user.previous != 'E':
        return redirect(url_for('ai_advice.last_set'))

    if question_number != 6 and question_number != 11 and question_number != 18 and getattr(user, "advice{}".format(question_number)) is None and getattr(user, "question{}".format(question_number)) is not None:
        return redirect(url_for('ai_advice.AIAdvice'))

#    elif (question_number == 6 or question_number == 11 or question_number == 18) and getattr(user, "attention{}".format(
#            question_number)) is not None:
#        return 'bad request!', 400

#    elif question_number != 6 and question_number != 11 and question_number != 18 and getattr(user, "question{}".format(
#            question_number)) is not None:
#        return 'bad request!', 400

    # Load in questions from data set
    data_context = questions_list.iloc[question_number][0]
    data_question = questions_list.iloc[question_number][1]
    data_answer0 = questions_list.iloc[question_number][2]
    data_answer1 = questions_list.iloc[question_number][3]
    data_answer2 = questions_list.iloc[question_number][4]
    data_answer3 = questions_list.iloc[question_number][5]
    data_advice = questions_list.iloc[question_number][7]

    # Check if question has been answered and store answer
    if form.validate_on_submit() and (form.answer.data == 'A' or form.answer.data == 'B' or form.answer.data == 'C'
                                      or form.answer.data == 'D'):
        if question_number == 6 or question_number == 11 or question_number == 18:
            setattr(user, "attention{}".format(question_number), form.answer.data)
            user.task_counter = counter + 1
            db.session.commit()
            return redirect(url_for('ai_advice.questions'))
        else:
            setattr(user, "question{}".format(question_number), form.answer.data)
            user.previous = form.answer.data
            db.session.commit()
            return redirect(url_for('ai_advice.AIAdvice'))
    # Gives warning when form is submitted with no answer in place
    if request.method == 'POST':
        flash('No answer found, please select an answer', 'danger')
    return render_template('questions.html', form=form, context=data_context, question=data_question,
                           answer0=data_answer0, answer1=data_answer1, answer2=data_answer2, answer3=data_answer3,
                           counter=counter, list=list, advice=data_advice, old_answer=old_answer)


# Route to show the pages including AI advice
@ai_advice.route("/prediction", methods=['POST', 'GET'])
@login_required
def AIAdvice():
    form = OtherForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    question_number = question_order_list[user.question_order][counter]
    old_answer = user.previous

    if question_number == 6 or question_number == 11 or question_number == 18:
        return redirect(url_for('ai_advice.questions'))

    if getattr(user, "advice{}".format(question_number)) is not None or getattr(user, "question{}".format(question_number)) is None:
        if 6 < counter < 12 and user.tutorial == 0:
            if getattr(user, "advice{}".format(question_number)) == questions_list.iloc[question_number][7]:
                return redirect(url_for('ai_advice.correct'))
            else:
                return redirect(url_for('ai_advice.tutorial'))
        else:
            return redirect(url_for('ai_advice.questions'))

    if counter > 18:
        return redirect(url_for('ai_advice.survey'))

    # Load in questions from data set
    data_context = questions_list.iloc[question_number][0]
    data_question = questions_list.iloc[question_number][1]
    data_answer0 = questions_list.iloc[question_number][2]
    data_answer1 = questions_list.iloc[question_number][3]
    data_answer2 = questions_list.iloc[question_number][4]
    data_answer3 = questions_list.iloc[question_number][5]
    data_advice = questions_list.iloc[question_number][9]

    # Check if question has been answered and store answer
    if form.validate_on_submit() and (form.answer.data == 'A' or form.answer.data == 'B' or form.answer.data == 'C'
                                      or form.answer.data == 'D'):
        if getattr(user, "advice{}".format(question_number)) is not None:
            flash('There is already an answer for this question you can not answer this again, please continue', 'danger')
        else:
            setattr(user, "advice{}".format(question_number), form.answer.data)
            db.session.commit()

        if 6 < counter < 12 and user.tutorial == 0:
            if getattr(user, "advice{}".format(question_number)) == questions_list.iloc[question_number][7]:
                user.task_counter = counter + 1
                db.session.commit()
                return redirect(url_for('ai_advice.correct'))
            else:
                return redirect(url_for('ai_advice.tutorial'))
        else:
            user.task_counter = counter + 1
            db.session.commit()
            return redirect(url_for('ai_advice.questions'))

    # Gives warning when form is submitted with no answer in place
    if request.method == 'POST':
        flash('No answer found, please select an answer', 'danger')
    return render_template('AIquestions.html', form=form, context=data_context, question=data_question,
                           answer0=data_answer0, answer1=data_answer1, answer2=data_answer2, answer3=data_answer3,
                           counter=counter, list=list, advice=data_advice, old_answer=old_answer)


@ai_advice.route("/tutorial", methods=['GET', 'POST'])
@login_required
def tutorial():
    form = LoginForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    question_number = question_order_list[user.question_order][counter]
    old_answer = getattr(user, "advice{}".format(question_number))

    if old_answer is None:
        return redirect(url_for('ai_advice.questions'))

    correct_answer = questions_list.iloc[question_number][7]
    data_context = questions_list.iloc[question_number][0]
    data_question = questions_list.iloc[question_number][1]
    data_answer0 = questions_list.iloc[question_number][2]
    data_answer1 = questions_list.iloc[question_number][3]
    data_answer2 = questions_list.iloc[question_number][4]
    data_answer3 = questions_list.iloc[question_number][5]
    data_advice = questions_list.iloc[question_number][9]
    if old_answer == 'A':
        tutorial_ai = questions_list.iloc[question_number][10]
    elif old_answer == 'B':
        tutorial_ai = questions_list.iloc[question_number][11]
    elif old_answer == 'C':
        tutorial_ai = questions_list.iloc[question_number][12]
    else:
        tutorial_ai = questions_list.iloc[question_number][13]

    if form.validate_on_submit():
        user.task_counter = counter + 1
        db.session.commit()
        return redirect(url_for('ai_advice.questions'))

    return render_template('tutorial.html', form=form, context=data_context, question=data_question,
                           answer0=data_answer0, answer1=data_answer1, answer2=data_answer2, answer3=data_answer3,
                           counter=counter, list=list, advice=data_advice, old_answer=old_answer,
                           tutorial_ai=tutorial_ai, correct_answer=correct_answer)


@ai_advice.route("/survey", methods=['GET', 'POST'])
@login_required
def survey():
    form = Survey()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter

    if form.validate_on_submit() and (form.self.data == '0' or form.self.data == '1' or form.self.data == '2' or
                                      form.self.data == '3' or form.self.data == '4' or form.self.data == '5' or
                                      form.self.data == '6') and (form.other.data == '0' or form.other.data == '1' or
                                                                  form.other.data == '2' or form.other.data == '3 ' or
                                                                  form.other.data == '4' or form.other.data == '5' or
                                                                  form.other.data == '6'):
        if counter < 8:
            if user.surveySelf1 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
            else:
                user.surveySelf1 = form.self.data
                user.surveyOther1 = form.other.data
                user.surveyPercentage1 = request.form["percentage"]
                db.session.commit()
            if user.tutorial == 0:
                return redirect(url_for('ai_advice.tutorial_start'))
            else:
                return redirect(url_for('ai_advice.no_tutorial_start'))
        else:
            if user.surveySelf2 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
                return redirect(url_for('ai_advice.final'))
            user.surveySelf2 = form.self.data
            user.surveyOther2 = form.other.data
            user.surveyPercentage2 = request.form["percentage"]
            db.session.commit()
            return redirect(url_for('ai_advice.final'))

    # Gives warning when form is submitted with no answer in place
    elif request.method == 'POST':
        flash('Not to all questions a valid answer was found, please fill out all questions', 'danger')

    return render_template('survey.html', form=form)


# Allows to start from where user left off
@ai_advice.route("/correct", methods=['GET', 'POST'])
@login_required
def correct():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('correct.html', form=form)


# Allows to start from where user left off
@ai_advice.route("/continue", methods=['GET', 'POST'])
@login_required
def go_on():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('continue.html', form=form)


# Route final page that shows user the survey is done
@ai_advice.route("/end", methods=['GET', 'POST'])
def final():
    return render_template('final.html')


@ai_advice.route("/tutorial_start", methods=['GET', 'POST'])
@login_required
def tutorial_start():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('tutorialStart.html', form=form)


@ai_advice.route("/next", methods=['GET', 'POST'])
@login_required
def no_tutorial_start():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('next.html', form=form)


@ai_advice.route("/last_set", methods=['GET', 'POST'])
@login_required
def last_set():
    form = LoginForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        user.previous = 'E'
        db.session.commit()
        return redirect(url_for('ai_advice.questions'))
    return render_template('lastSet.html', form=form)
