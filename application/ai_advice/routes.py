from flask import render_template, url_for, redirect, request, flash, Blueprint
from application import load_data, db
from flask_login import login_user, current_user, login_required
from application.main.models import User, AIUser
from application.main.forms import LoginForm, OtherForm, Survey, ATI, TIA
from random import randint

ai_advice = Blueprint('ai_advice', __name__, url_prefix='/ai')
questions_list = load_data("/static/AIadvice.csv")  # CSV list with data

# Random orders (with constraints) of questions
question0 = [1, 4, 5, 2, 6, 3, 0, 7, 10, 11, 8, 9, 14, 17, 13, 18, 12, 16, 15]
question1 = [12, 17, 13, 14, 18, 16, 15, 9, 10, 11, 8, 7, 5, 0, 2, 6, 1, 4, 3]
question2 = [1, 4, 5, 0, 6, 3, 2, 8, 10, 11, 9, 7, 15, 13, 17, 18, 14, 16, 12]
question3 = [12, 16, 17, 14, 18, 13, 15, 10, 8, 11, 9, 7, 2, 4, 5, 6, 0, 3, 1]
question4 = [3, 1, 4, 2, 6, 0, 5, 8, 10, 11, 9, 7, 17, 13, 15, 18, 12, 16, 14]
question5 = [16, 13, 14, 17, 18, 12, 15, 9, 10, 11, 8, 7, 0, 5, 1, 6, 3, 4, 2]
question6 = [4, 1, 3, 0, 6, 2, 5, 8, 7, 11, 10, 9, 17, 16, 13, 18, 15, 14, 12]
question7 = [12, 14, 16, 17, 18, 15, 13, 8, 7, 11, 10, 9, 3, 2, 4, 6, 1, 5, 0]
question8 = [2, 0, 4, 5, 6, 3, 1, 8, 9, 11, 7, 10, 16, 15, 17, 18, 12, 13, 14]
question9 = [12, 14, 16, 15, 18, 13, 17, 10, 9, 11, 8, 7, 0, 4, 5, 6, 3, 2, 1]
question_order_list = [question0, question1, question2, question3, question4, question5, question6, question7,
                       question8, question9]


# Route to create user from userID given by prolific and continues to next page with tutorial
@ai_advice.route("/version1/", methods=['GET', 'POST'])
def start_tut():
    username = request.args.get('PROLIFIC_PID')
    exsits = User.query.filter_by(username=username).first()
    # Check if new account and needs to be created, and create if needed
    if exsits is None:
        user = User(username=username, ai_started=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        order = randint(0, 9)
        ai_user = AIUser(username=username, AI_user=current_user, tutorial=0, question_order=order)
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


# Route to create user from userID given by prolific and continues to next page without tutorial
@ai_advice.route("/version2/", methods=['GET', 'POST'])
def start_no_tut():
    username = request.args.get('PROLIFIC_PID')
    exsits = User.query.filter_by(username=username).first()
    # Check if new account and needs to be created, and create if needed
    if exsits is None:
        user = User(username=username, ai_started=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        order = randint(0, 9)
        ai_user = AIUser(username=username, AI_user=current_user, tutorial=1, question_order=order)
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
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    timer = 5000
    if user.previous == 'F':
        return redirect(url_for('ai_advice.attention_check'))
    if request.method == 'POST':
        user.previous = 'F'
        db.session.commit()
        return redirect(url_for('ai_advice.attention_check'))
    return render_template('introductionAI.html', form=form, timer=timer)


# Route to iterate over all questions
@ai_advice.route("/questions", methods=['POST', 'GET'])
@login_required
def questions():
    form = OtherForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    show = counter
    timer = 30000

    if counter > 18:
        current_user.ai_done = True
        db.session.commit()
        return redirect(url_for('ai_advice.survey1'))

    question_number = question_order_list[user.question_order][counter]
    old_answer = user.previous

    if counter > 15:
        show = show - 3
    elif counter > 9:
        show = show - 2
    elif counter > 4:
        show = show - 1

    if counter == 7 and user.previous != 'E':
        user.previous = 'E'
        db.session.commit()
        return redirect(url_for('ai_advice.survey1'))

    elif counter == 12 and user.previous != 'E':
        return redirect(url_for('ai_advice.last_set'))

    if question_number == 6 or question_number == 11 or question_number == 18:
        timer = 10000

    if question_number != 6 and question_number != 11 and question_number != 18 and getattr(user, "advice{}".format(
            question_number)) is None and getattr(user, "question{}".format(question_number)) is not None:
        return redirect(url_for('ai_advice.AIAdvice'))

    # Check if enough attention checks answered correctly
    if (counter > 9) and (counter < 17):
        wrong_answers = 0
        if user.attention6 != 'B' and user.attention6 is not None:
            wrong_answers += 1
        if user.attention11 != 'D' and user.attention11 is not None:
            wrong_answers += 1
        if user.attention18 != 'C' and user.attention18 is not None:
            wrong_answers += 1
        if wrong_answers >= 2:
            return redirect(url_for('ai_advice.final'))  # change for prolific kickout

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
                           counter=counter, list=list, advice=data_advice, old_answer=old_answer, show=show,
                           timer=timer)


# Route to show the pages including AI advice
@ai_advice.route("/prediction", methods=['POST', 'GET'])
@login_required
def AIAdvice():
    form = OtherForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    question_number = question_order_list[user.question_order][counter]
    old_answer = user.previous
    show = counter
    timer = 10000

    if question_number == 6 or question_number == 11 or question_number == 18:
        return redirect(url_for('ai_advice.questions'))

    if getattr(user, "advice{}".format(question_number)) is not None or getattr(user, "question{}".format(
            question_number)) is None:
        if 6 < counter < 12 and user.tutorial == 0:
            if getattr(user, "advice{}".format(question_number)) == questions_list.iloc[question_number][7]:
                return redirect(url_for('ai_advice.correct'))
            else:
                return redirect(url_for('ai_advice.tutorial'))
        else:
            return redirect(url_for('ai_advice.questions'))

    if counter > 18:
        return redirect(url_for('ai_advice.survey1'))

    if counter > 15:
        show = show - 3
    elif counter > 9:
        show = show - 2
    elif counter > 4:
        show = show - 1

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
            flash('There is already an answer for this question you can not answer this again, please continue',
                  'danger')
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
                           counter=counter, list=list, advice=data_advice, old_answer=old_answer, show=show,
                           timer=timer)


# Tutorial page, that also gives feedback
@ai_advice.route("/tutorial", methods=['GET', 'POST'])
@login_required
def tutorial():
    form = LoginForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    question_number = question_order_list[user.question_order][counter]
    old_answer = getattr(user, "advice{}".format(question_number))
    show = counter
    timer = 5000

    if counter > 15:
        show = show - 3
    elif counter > 9:
        show = show - 2
    elif counter > 4:
        show = show - 1

    if old_answer is None:
        return redirect(url_for('ai_advice.questions'))

    # Load in questions from data set
    correct_answer = questions_list.iloc[question_number][7]
    data_context = questions_list.iloc[question_number][0]
    data_question = questions_list.iloc[question_number][1]
    data_answer0 = questions_list.iloc[question_number][2]
    data_answer1 = questions_list.iloc[question_number][3]
    data_answer2 = questions_list.iloc[question_number][4]
    data_answer3 = questions_list.iloc[question_number][5]
    data_advice = questions_list.iloc[question_number][9]
    # Show different feedback depending on answer of participant
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
                           tutorial_ai=tutorial_ai, correct_answer=correct_answer, show=show, timer=timer)


# First survey page with first question
@ai_advice.route("/survey1", methods=['GET', 'POST'])
@login_required
def survey1():
    form = Survey()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter
    timer = 2000

    # Check for valid answer
    if form.validate_on_submit() and (form.answer.data == '0' or form.answer.data == '1' or form.answer.data == '2' or
                                      form.answer.data == '3' or form.answer.data == '4' or form.answer.data == '5' or
                                      form.answer.data == '6'):
        # Check first or second survey
        if counter < 8:
            if user.surveySelf1 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
            else:
                user.surveySelf1 = form.answer.data
                db.session.commit()
            return redirect(url_for('ai_advice.survey2'))

        else:
            if user.surveySelf2 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
            else:
                user.surveySelf2 = form.answer.data
                db.session.commit()
        return redirect(url_for('ai_advice.survey2'))

    # Gives warning when form is submitted with no answer in place
    elif request.method == 'POST':
        flash('No answer found, please select an answer', 'danger')

    return render_template('survey.html', form=form, timer=timer)


# Second survey page with second question
@ai_advice.route("/survey2", methods=['GET', 'POST'])
@login_required
def survey2():
    form = Survey()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter
    timer = 2000

    # Check for valid answer
    if form.validate_on_submit() and (form.answer.data == '0' or form.answer.data == '1' or form.answer.data == '2' or
                                      form.answer.data == '3' or form.answer.data == '4' or form.answer.data == '5' or
                                      form.answer.data == '6'):
        # Check if first or second survey
        if counter < 8:
            if user.surveyOther1 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
            else:
                user.surveyOther1 = form.answer.data
                db.session.commit()
            return redirect(url_for('ai_advice.survey3'))

        else:
            if user.surveyOther2 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
            else:
                user.surveyOther2 = form.answer.data
                db.session.commit()
        return redirect(url_for('ai_advice.survey3'))

    # Gives warning when form is submitted with no answer in place
    elif request.method == 'POST':
        flash('No answer found, please select an answer', 'danger')

    return render_template('survey2.html', form=form, timer=timer)


# Third survey page with third question
@ai_advice.route("/survey3", methods=['GET', 'POST'])
@login_required
def survey3():
    form = Survey()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter
    timer = 2000

    # Check for valid answer
    if form.validate_on_submit() and (0 <= int(request.form["answer"]) <= 100):
        # Check first or second survey
        if counter < 8:
            if user.surveyPercentage1 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
            else:
                user.surveyPercentage1 = request.form["answer"]
                db.session.commit()
            return redirect(url_for('ai_advice.tia'))

        else:
            if user.surveyPercentage2 is not None:
                flash('There is already an answer for this survey you can not answer it again', 'danger')
                return redirect(url_for('ai_advice.tia'))
            user.surveyPercentage2 = request.form["answer"]
            db.session.commit()
        return redirect(url_for('ai_advice.tia'))

    # Gives warning when form is submitted with no answer in place
    elif request.method == 'POST':
        flash('No answer found, please select a value between 0 and 100', 'danger')

    return render_template('survey3.html', form=form, timer=timer)


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


# Start page of second part for version with tutorial
@ai_advice.route("/tutorial_start", methods=['GET', 'POST'])
@login_required
def tutorial_start():
    timer = 2000
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('tutorialStart.html', form=form, timer=timer)


# Start page of second part for version without tutorial
@ai_advice.route("/next", methods=['GET', 'POST'])
@login_required
def no_tutorial_start():
    form = LoginForm()
    if request.method == 'POST':
        return redirect(url_for('ai_advice.questions'))
    return render_template('next.html', form=form)


# Page to make clear start of last set of questions
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


# Attention check directly after introduction
@ai_advice.route("/question", methods=['GET', 'POST'])
@login_required
def attention_check():
    timer = 5000
    form = OtherForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit() and form.answer.data == 'C':
        return redirect(url_for('ai_advice.ati'))
    elif form.validate_on_submit() and (form.answer.data == 'A' or form.answer.data == 'B' or form.answer.data == 'D'):
        return redirect(url_for('ai_advice.final'))  # to be replaced with kickout
    elif request.method == 'POST':
        flash('No answer found, please select an answer', 'danger')

    return render_template('attention.html', form=form, timer=timer)


# Starting questions on technology
@ai_advice.route("/startQ", methods=['GET', 'POST'])
@login_required
def ati():
    form = ATI()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    timer = 20000
    # Check if all answers are valid answers
    if form.validate_on_submit() and (form.ati1.data == '0' or form.ati1.data == '1' or form.ati1.data == '2' or
                                      form.ati1.data == '3' or form.ati1.data == '4' or form.ati1.data == '5') and (
            form.ati2.data == '0' or form.ati2.data == '1' or form.ati2.data == '2' or form.ati2.data == '3' or
            form.ati2.data == '4' or form.ati2.data == '5') and (form.ati3.data == '0' or form.ati3.data == '1' or
                                                                 form.ati3.data == '2' or form.ati3.data == '3' or
                                                                 form.ati3.data == '4' or form.ati3.data == '5') and (
            form.ati4.data == '0' or form.ati4.data == '1' or form.ati4.data == '2' or form.ati4.data == '3' or
            form.ati4.data == '4' or form.ati4.data == '5') and (form.ati5.data == '0' or form.ati5.data == '1' or
                                                                 form.ati5.data == '2' or form.ati5.data == '3' or
                                                                 form.ati5.data == '4' or form.ati5.data == '5') and (
            form.ati6.data == '0' or form.ati6.data == '1' or form.ati6.data == '2' or form.ati6.data == '3' or
            form.ati6.data == '4' or form.ati6.data == '5') and (form.ati7.data == '0' or form.ati7.data == '1' or
                                                                 form.ati7.data == '2' or form.ati7.data == '3' or
                                                                 form.ati7.data == '4' or form.ati7.data == '5') and (
            form.ati8.data == '0' or form.ati8.data == '1' or form.ati8.data == '2' or form.ati8.data == '3' or
            form.ati8.data == '4' or form.ati8.data == '5') and (form.ati9.data == '0' or form.ati9.data == '1' or
                                                                 form.ati9.data == '2' or form.ati9.data == '3' or
                                                                 form.ati9.data == '4' or form.ati9.data == '5'):

        if user.ati1 is not None:
            flash('There are already answers for this questionnaire you can not answer them again', 'danger')
            return redirect(url_for('ai_advice.questions'))
        else:
            user.ati1 = form.ati1.data
            user.ati2 = form.ati2.data
            user.ati3 = form.ati3.data
            user.ati4 = form.ati4.data
            user.ati5 = form.ati5.data
            user.ati6 = form.ati6.data
            user.ati7 = form.ati7.data
            user.ati8 = form.ati8.data
            user.ati9 = form.ati9.data
            db.session.commit()

        return redirect(url_for('ai_advice.questions'))

    elif request.method == 'POST':
        flash('Not all answers found, please select an answer for all questions', 'danger')
    return render_template('ATI.html', form=form, timer=timer)


# Questions inbetween
@ai_advice.route("/Q", methods=['GET', 'POST'])
@login_required
def tia():
    form = TIA()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter
    timer = 10000
    # Check if all answers are valid answers
    if form.validate_on_submit() and (form.tia1.data == '0' or form.tia1.data == '1' or form.tia1.data == '2' or
                                      form.tia1.data == '3' or form.tia1.data == '4' or form.tia1.data == '5') and (
            form.tia2.data == '0' or form.tia2.data == '1' or form.tia2.data == '2' or form.tia2.data == '3' or
            form.tia2.data == '4' or form.tia2.data == '5') and (form.tia3.data == '0' or form.tia3.data == '1' or
                                                                 form.tia3.data == '2' or form.tia3.data == '3' or
                                                                 form.tia3.data == '4' or form.tia3.data == '5') and (
            form.tia4.data == '0' or form.tia4.data == '1' or form.tia4.data == '2' or form.tia4.data == '3' or
            form.tia4.data == '4' or form.tia4.data == '5') and (form.tia5.data == '0' or form.tia5.data == '1' or
                                                                 form.tia5.data == '2' or form.tia5.data == '3' or
                                                                 form.tia5.data == '4' or form.tia5.data == '5'):
        if counter < 8:
            if user.tia1_1 is not None:
                flash('There are already answers for this questionnaire you can not answer them again', 'danger')
                # Redirect depending on version
                if user.tutorial == 0:
                    return redirect(url_for('ai_advice.tutorial_start'))
                else:
                    return redirect(url_for('ai_advice.no_tutorial_start'))
            else:
                user.tia1_1 = form.tia1.data
                user.tia1_2 = form.tia2.data
                user.tia1_3 = form.tia3.data
                user.tia1_4 = form.tia4.data
                user.tia1_5 = form.tia5.data
                db.session.commit()
                # Redirect depending on version
                if user.tutorial == 0:
                    return redirect(url_for('ai_advice.tutorial_start'))
                else:
                    return redirect(url_for('ai_advice.no_tutorial_start'))
        else:
            if user.tia2_1 is not None:
                flash('There are already answers for this questionnaire you can not answer them again', 'danger')
                return redirect(url_for('ai_advice.final'))
            else:
                user.tia2_1 = form.tia1.data
                user.tia2_2 = form.tia2.data
                user.tia2_3 = form.tia3.data
                user.tia2_4 = form.tia4.data
                user.tia2_5 = form.tia5.data
                db.session.commit()
            return redirect(url_for('ai_advice.final'))

    elif request.method == 'POST':
        flash('Not all answers found, please select an answer for all questions', 'danger')
    return render_template('TIA.html', form=form, timer=timer)
