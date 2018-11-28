from flaskscraper import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    user_img = db.Column(db.String())
    answers = db.Column(db.Integer)
    questions = db.Column(db.Integer)
    reached = db.Column(db.String(15))
    url = db.Column(db.String())
    questions_list = db.relationship('Question', backref='asker', lazy=True)
    answers_list = db.relationship('Answer', backref='responder', lazy=True)
    commenter = db.relationship('Comment', backref='commenter', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.reached}', '{self.url}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String())
    question = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vote_score = db.Column(db.Integer)
    answer_count = db.Column(db.Integer)
    view_count = db.Column(db.String())
    date = db.Column(db.String())
    url = db.Column(db.String())
    full_url = db.Column(db.String())
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answers_ref = db.relationship('Answer', backref='answers', foreign_keys=[answer_id], lazy=True)
    rating = db.relationship('QuestionRating', backref='rating', lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer)
    answer = db.Column(db.String())
    vote_score = db.Column(db.Integer)
    date = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions_ref = db.relationship('Question', backref='questionsref', foreign_keys=[post_id], lazy=True)

    def __repr__(self):
        return f"Answer('{self.id}', '{self.post_id}', '{self.answer_id}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String())
    date = db.Column(db.String())
    #rating = db.relationship('Rating', backref='rating', lazy=True)

    def __repr__(self):
        return f"Comment('{self.post_id}', '{self.answer_id}', '{self.user_id}')"

class QuestionRating(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    accurate = db.Column(db.String())
    relevant = db.Column(db.String())
    complexity = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)

    def __repr__(self):
        return f"Rating('{self.question_id}', '{self.accurate}', '{self.relevant}', '{self.complexity}')"
