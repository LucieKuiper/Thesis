from flask_login import UserMixin
from application import db, login_manager

# Model for users that stores answers to all questions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20), nullable=False, unique=True)
    task_counter = db.Column(db.Integer, default=0)
    question0 = db.Column(db.String(20),  nullable=True, default=None)
    question1 = db.Column(db.String(20),  nullable=True, default=None)
    question2 = db.Column(db.String(20),  nullable=True, default=None)
    question3 = db.Column(db.String(20),  nullable=True, default=None)
    question4 = db.Column(db.String(20),  nullable=True, default=None)
    question5 = db.Column(db.String(20),  nullable=True, default=None)
    question6 = db.Column(db.String(20),  nullable=True, default=None)
    question7 = db.Column(db.String(20),  nullable=True, default=None)
    question8 = db.Column(db.String(20),  nullable=True, default=None)
    question9 = db.Column(db.String(20),  nullable=True, default=None)
    question10 = db.Column(db.String(20),  nullable=True, default=None)
    question11 = db.Column(db.String(20),  nullable=True, default=None)
    question12 = db.Column(db.String(20),  nullable=True, default=None)
    question13 = db.Column(db.String(20),  nullable=True, default=None)
    question14 = db.Column(db.String(20),  nullable=True, default=None)
    question15 = db.Column(db.String(20), nullable=True, default=None)
    question16 = db.Column(db.String(20),  nullable=True, default=None)
    question17 = db.Column(db.String(20),  nullable=True, default=None)
    question18 = db.Column(db.String(20),  nullable=True, default=None)
    question19 = db.Column(db.String(20),  nullable=True, default=None)
    question20 = db.Column(db.String(20),  nullable=True, default=None)
    question21 = db.Column(db.String(20),  nullable=True, default=None)
    question22 = db.Column(db.String(20), nullable=True, default=None)
    question23 = db.Column(db.String(20),  nullable=True, default=None)
    question24 = db.Column(db.String(20),  nullable=True, default=None)
    question25 = db.Column(db.String(20),  nullable=True, default=None)
    question26 = db.Column(db.String(20),  nullable=True, default=None)
    question27 = db.Column(db.String(20),  nullable=True, default=None)
    question28 = db.Column(db.String(20), nullable=True, default=None)
    question29 = db.Column(db.String(20), nullable=True, default=None)

    def __repr__(self):
        return f"user('{self.userid}')"
