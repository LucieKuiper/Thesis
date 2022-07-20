from flask import Blueprint
from flask import render_template, url_for, redirect, request
from application import load_data, db
from flask_login import login_user, current_user, login_required
from application.main.models import User, AIUser
from application.main.forms import LoginForm, ShortForm

ai_advice = Blueprint('ai_advice', __name__, url_prefix='/ai')
questions_list = load_data("/static/AIadvice.csv")  # CSV list with data


# Route to create user from userID given by prolific and continues to next page
@ai_advice.route("/", methods=['GET', 'POST'])
def start():
    username = request.args.get('PROLIFIC_PID')
    exsits = User.query.filter_by(username=username).first()
    # Check if new account and needs to be created otherwise show that already done survey
    if exsits is None:
        user = User(username=username, ai_started = True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        ai_user = AIUser(username=username, AI_user=current_user)
        db.session.add(ai_user)
        db.session.commit()
        return redirect(url_for('ai_advice.introduction'))
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
    return render_template('introduction.html', form=form)


# Route to iterate over all questions
@ai_advice.route("/questions", methods=['POST', 'GET'])
@login_required
def questions():
    form = ShortForm()
    user = AIUser.query.filter_by(user_id=current_user.id).first()
    counter = user.task_counter  # counter that tracks at which question the user is
    if counter > 3:
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
    if form.validate_on_submit():
        setattr(user, "question{}".format(counter), form.answer.data)
        user.task_counter = counter + 1
        db.session.commit()
        return redirect(url_for('ai_advice.questions'))
    return render_template('AIquestions.html', form=form, context=data_context, question=data_question,
                           answer0=data_answer0, answer1=data_answer1, answer2=data_answer2, answer3=data_answer3,
                           counter=counter, list=list, advice=data_advice)


# Introduction with information
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
