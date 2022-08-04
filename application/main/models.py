from flask_login import UserMixin
from application import db
from application import login_manager


# Model for users that stores answers to all questions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    pilot_done = db.Column(db.Boolean, default=False)
    pilot_started = db.Column(db.Boolean, default=False)
    ai_done = db.Column(db.Boolean, default=False)
    ai_started = db.Column(db.Boolean, default=False)
    pilot = db.relationship('PilotUser', backref='pilot_user', lazy=True)
    ai = db.relationship('AIUser', backref='AI_user', lazy=True)


class PilotUser(db.Model, UserMixin):
    __tablename__ = 'pilot_user'

    pilot_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_counter = db.Column(db.Integer, default=0)
    question_order = db.Column(db.Integer, default=0)
    question0 = db.Column(db.String(1), nullable=True, default=None)
    question1 = db.Column(db.String(1), nullable=True, default=None)
    question2 = db.Column(db.String(1), nullable=True, default=None)
    question3 = db.Column(db.String(1), nullable=True, default=None)
    question4 = db.Column(db.String(1), nullable=True, default=None)
    question5 = db.Column(db.String(1), nullable=True, default=None)
    question6 = db.Column(db.String(1), nullable=True, default=None)
    question7 = db.Column(db.String(1), nullable=True, default=None)
    question8 = db.Column(db.String(1), nullable=True, default=None)
    question9 = db.Column(db.String(1), nullable=True, default=None)
    question10 = db.Column(db.String(1), nullable=True, default=None)
    question11 = db.Column(db.String(1), nullable=True, default=None)
    question12 = db.Column(db.String(1), nullable=True, default=None)
    question13 = db.Column(db.String(1), nullable=True, default=None)
    question14 = db.Column(db.String(1), nullable=True, default=None)
    question15 = db.Column(db.String(1), nullable=True, default=None)
    question16 = db.Column(db.String(1), nullable=True, default=None)
    question17 = db.Column(db.String(1), nullable=True, default=None)
    question18 = db.Column(db.String(1), nullable=True, default=None)
    question19 = db.Column(db.String(1), nullable=True, default=None)
    question20 = db.Column(db.String(1), nullable=True, default=None)
    question21 = db.Column(db.String(1), nullable=True, default=None)
    question22 = db.Column(db.String(1), nullable=True, default=None)
    question23 = db.Column(db.String(1), nullable=True, default=None)
    question24 = db.Column(db.String(1), nullable=True, default=None)
    question25 = db.Column(db.String(1), nullable=True, default=None)
    question26 = db.Column(db.String(1), nullable=True, default=None)
    question27 = db.Column(db.String(1), nullable=True, default=None)
    question28 = db.Column(db.String(1), nullable=True, default=None)
    question29 = db.Column(db.String(1), nullable=True, default=None)

    confident0 = db.Column(db.String(3), nullable=True, default=None)
    confident1 = db.Column(db.String(3), nullable=True, default=None)
    confident2 = db.Column(db.String(3), nullable=True, default=None)
    confident3 = db.Column(db.String(3), nullable=True, default=None)
    confident4 = db.Column(db.String(3), nullable=True, default=None)
    confident5 = db.Column(db.String(3), nullable=True, default=None)
    confident6 = db.Column(db.String(3), nullable=True, default=None)
    confident7 = db.Column(db.String(3), nullable=True, default=None)
    confident8 = db.Column(db.String(3), nullable=True, default=None)
    confident9 = db.Column(db.String(3), nullable=True, default=None)
    confident10 = db.Column(db.String(3), nullable=True, default=None)
    confident11 = db.Column(db.String(3), nullable=True, default=None)
    confident12 = db.Column(db.String(3), nullable=True, default=None)
    confident13 = db.Column(db.String(3), nullable=True, default=None)
    confident14 = db.Column(db.String(3), nullable=True, default=None)
    confident15 = db.Column(db.String(3), nullable=True, default=None)
    confident16 = db.Column(db.String(3), nullable=True, default=None)
    confident17 = db.Column(db.String(3), nullable=True, default=None)
    confident18 = db.Column(db.String(3), nullable=True, default=None)
    confident19 = db.Column(db.String(3), nullable=True, default=None)
    confident20 = db.Column(db.String(3), nullable=True, default=None)
    confident21 = db.Column(db.String(3), nullable=True, default=None)
    confident22 = db.Column(db.String(3), nullable=True, default=None)
    confident23 = db.Column(db.String(3), nullable=True, default=None)
    confident24 = db.Column(db.String(3), nullable=True, default=None)
    confident25 = db.Column(db.String(3), nullable=True, default=None)
    confident26 = db.Column(db.String(3), nullable=True, default=None)
    confident27 = db.Column(db.String(3), nullable=True, default=None)
    confident28 = db.Column(db.String(3), nullable=True, default=None)
    confident29 = db.Column(db.String(3), nullable=True, default=None)


    def __repr__(self):
        return f"user('{self.username}')"


class AIUser(db.Model, UserMixin):
    __tablename__ = 'AIuser'
    ai_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_counter = db.Column(db.Integer, default=0)
    question0 = db.Column(db.String(1), nullable=True, default=None)
    question1 = db.Column(db.String(1), nullable=True, default=None)
    question2 = db.Column(db.String(1), nullable=True, default=None)
    question3 = db.Column(db.String(1), nullable=True, default=None)
    question4 = db.Column(db.String(1), nullable=True, default=None)

    def __repr__(self):
        return f"user('{self.username}')"
