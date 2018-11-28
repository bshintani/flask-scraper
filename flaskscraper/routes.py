from flask import render_template, request, jsonify
from flaskscraper import app, db
from flaskscraper.models import User, Question, Answer, Comment, QuestionRating

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

    if 'questionRatingSubmit' in request.form and request.method == 'POST':
        question_acc = request.form['submit_question_acc']
        question_rel = request.form['submit_question_rel']
        question_comp = request.form['submit_question_comp']

        questionrating = QuestionRating(accurate=question_acc, relevant=question_rel, complexity=question_comp, question_id=question.id)
        question_exists = QuestionRating.query.filter(QuestionRating.question_id == question.id).first()
        if question_exists:
            print(question_exists)
            question_exists.accurate = question_acc
            question_exists.relevant = question_rel
            question_exists.complexity = question_comp
            db.session.commit()
        else:
            db.session.add(questionrating)
            db.session.commit()

    return render_template('questions/question.html', question=question, answers=answers, users=users, comments=comments)

# @app.route('/submitRatings', methods=['POST'])
# def submitRatings():
#
#     question_acc = request.form['submit_question_acc']
#     question_rel = request.form.get('submit_question_rel')
#     question_comp = request.form.get('submit_question_comp')
#
#     rating = Rating(accurate=question_acc, relevant=question_rel, complexity=question_comp, question_id=question.id)
#     db.session.add(rating)
#     db.session.commit()
