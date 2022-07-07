from flask_login import UserMixin
from application import db, login_manager


# Model for users that stores answers to all questions
@login_manager.user_loader
def load_user(user_id):
    return AIUser.query.get(int(user_id))


class AIUser(db.Model, UserMixin):
    __tablename__ = 'AIuser'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20), nullable=False, unique=True)
    task_counter = db.Column(db.Integer, default=0)
    question0 = db.Column(db.String(20), nullable=True, default=None)
    question1 = db.Column(db.String(20), nullable=True, default=None)
    question2 = db.Column(db.String(20), nullable=True, default=None)
    question3 = db.Column(db.String(20), nullable=True, default=None)
    question4 = db.Column(db.String(20), nullable=True, default=None)

    def __repr__(self):
        return f"user('{self.userid}')"
