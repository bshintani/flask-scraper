from flaskscraper import db
from flaskscraper.models import User, Question, Answer, Comment
import csv

with open('scraper-files/users.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user = User(id=row['User ID'], username=row['Username'], user_img=row['Image'], answers=row['Answers'], questions=row['Questions'], reached=row['Reached'], url=row['URL'])
        db.session.add(user)
        db.session.commit()

with open('scraper-files/questions.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question = Question(id=row['Post ID'], title=row['Title'], question=row['Question'], user_id=row['User ID'], vote_score=row['Vote Score'], answer_count=row['Answer Count'], view_count=row['View Count'], date=row['Date'], url=row['URL'], full_url=row['Full URL'])
        db.session.add(question)
        db.session.commit()

with open('scraper-files/answers.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        answer = Answer(post_id=row['Post ID'], answer_id=row['Answer ID'], answer=row['Answer'], vote_score=row['Vote Score'], date=row['Date'], user_id=row['User ID'])
        db.session.add(answer)
        db.session.commit()

with open('scraper-files/comments.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        comment = Comment(post_id=row['Post ID'], answer_id=row['Answer ID'], user_id=row['User ID'], comment=row['Comment'], date=row['Date'])
        db.session.add(comment)
        db.session.commit()
