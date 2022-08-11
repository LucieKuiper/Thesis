from flask import render_template, url_for, redirect, request, flash, Blueprint
from application import load_data, db
from flask_login import login_user, current_user, login_required
from application.main.models import User, AIUser
from application.main.forms import LoginForm, OtherForm

ai_advice = Blueprint('ai_advice', __name__, url_prefix='/ai')
questions_list = load_data("/static/AIadvice.csv")  # CSV list with data


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
        ai_user = AIUser(username=username, AI_user=current_user)
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
    old_answer = user.previous
    if counter > 15:
        current_user.ai_done = True
        db.session.commit()
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
    if form.validate_on_submit() and (form.answer.data == 'A' or form.answer.data == 'B' or form.answer.data == 'C'
                                      or form.answer.data == 'D'):
        setattr(user, "question{}".format(counter), form.answer.data)
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
    old_answer = user.previous
    # Load in questions from data set
    data_context = questions_list.iloc[counter][0]
    data_question = questions_list.iloc[counter][1]
    data_answer0 = questions_list.iloc[counter][2]
    data_answer1 = questions_list.iloc[counter][3]
    data_answer2 = questions_list.iloc[counter][4]
    data_answer3 = questions_list.iloc[counter][5]
    data_advice = questions_list.iloc[counter][9]

    # Check if question has been answered and store answer
    if form.validate_on_submit() and (form.answer.data == 'A' or form.answer.data == 'B' or form.answer.data == 'C'
                                      or form.answer.data == 'D'):
        setattr(user, "advice{}".format(counter), form.answer.data)
        db.session.commit()
        if 5 < counter < 10:
            if getattr(user, "question{}".format(counter)) == questions_list.iloc[counter][7]:
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
    old_answer = getattr(user, "advice{}".format(counter))
    data_context = questions_list.iloc[counter][0]
    data_question = questions_list.iloc[counter][1]
    data_answer0 = questions_list.iloc[counter][2]
    data_answer1 = questions_list.iloc[counter][3]
    data_answer2 = questions_list.iloc[counter][4]
    data_answer3 = questions_list.iloc[counter][5]
    data_advice = questions_list.iloc[counter][9]
    if old_answer == 'A':
        tutorial_ai = questions_list.iloc[counter][10]
    elif old_answer == 'B':
        tutorial_ai = questions_list.iloc[counter][11]
    elif old_answer == 'C':
        tutorial_ai = questions_list.iloc[counter][12]
    else:
        tutorial_ai = questions_list.iloc[counter][13]

    if request.method == 'POST':
        user.task_counter = counter + 1
        db.session.commit()
        return redirect(url_for('ai_advice.questions'))
    return render_template('tutorial.html', form=form, context=data_context, question=data_question,
                           answer0=data_answer0, answer1=data_answer1, answer2=data_answer2, answer3=data_answer3,
                           counter=counter, list=list, advice=data_advice, old_answer=old_answer, tutorial_ai=tutorial_ai)


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
