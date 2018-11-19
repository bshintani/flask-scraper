from flask import render_template
from flaskscraper import app
from flaskscraper.models import User, Question, Answer, Comment

@app.route("/")
@app.route("/home")
def home():
    users = User.query.all()
    questions = Question.query.all()
    answers = Answer.query.all()
    return render_template('home.html', questions=questions, answers=answers, users=users)

@app.route('/questions/<some_place>/<some_place_else>', methods=['GET', 'POST'])
def some_place_page(some_place, some_place_else):
    users = User.query.all()
    comments = Comment.query.all()
    question = Question.query.filter(Question.url.contains(some_place)).first()
    answers = Answer.query.filter(Answer.post_id == question.id).all()

    #if request.method == 'POST':

    return render_template('questions/question.html', question=question, answers=answers, users=users, comments=comments)
