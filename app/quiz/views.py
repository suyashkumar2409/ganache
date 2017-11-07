from flask import render_template, redirect, request, url_for, flash, jsonify
from . import quiz
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User, Quiz,Score
# from .forms import LoginForm, RegistrationForm
from ..email import send_email
from app import db
import csv
import json


QUESTIONSCORE = 10

@quiz.route('/')
def quizz():
	return redirect(url_for('main.index'))

@quiz.route('/view/<token>', methods = ['GET', 'POST'])
@login_required
def view(token):
	quizId = token.split('-')[0]
	quiz = Quiz.query.filter_by(id = quizId).first()
	
	if quiz is not None:

		score = Score.query.filter_by(giverId = current_user.get_id()).filter_by(quizId = quizId).first()

		if score is not None:
			# if already given
			if request.method == 'POST':
				flash("You can't submit the same test again! You scored " + score.score + ", deal with it!")

			isCreator = True # done to show shareable link thingy
			quizName = quiz.quizName
			questions = list(quiz.questionsIdList)
			numericalScore = score.score
			answers = score.answers

			correctAnswers = []
			for q in questions:
				correctAnswers.append(q['ans'])


			totalScore = len(questions) * QUESTIONSCORE

			lenQuestions = len(questions)
			return render_template('quiz/answers.html', isCreator = isCreator, quizName = quizName, numericalScore = numericalScore, answers = answers, questions = questions, totalScore = totalScore, correctAnswers = correctAnswers, token = token, lenQuestions = lenQuestions)

			# render the same answers

		else:
			if request.method == 'POST':
				# analyse answers here
				questions = list(quiz.questionsIdList)	
				answers = []
				numericalScore = 0
				for i in range(len(questions)):
					print request.form.get(str(i))
					answers.append(request.form.get(str(i)))
					if request.form.get(str(i)) == questions[i]['ans']:
						numericalScore = numericalScore + QUESTIONSCORE

				score = Score()
				score.giverId = current_user.get_id()
				score.quizId = quizId
				score.score = numericalScore
				score.answers = answers

				db.session.add(score)
				db.session.commit()
				# print "here"
				return redirect(url_for('quiz.view', token = token))


			else:
				# render quiz here
				isCreator = False

				quizName = quiz.quizName
				creatorId = quiz.creatorId

				if creatorId == current_user.get_id():
					isCreator = True
				else:
					isCreator = False

				questions = list(quiz.questionsIdList)
				# print questions

				# return redirect(url_for('main.index'))

				return render_template('quiz/quiz.html', isCreator = isCreator, quizName = quizName, questions = questions, token = token, questionsLen = len(questions))


	else:
		flash('Error - 404')
		return redirect(url_for('main.index'))


@quiz.route('/create', methods = ['GET', 'POST'])
@login_required
def createQuiz():
	if current_user.role_id == 2 or current_user.role_id == 3:
		if request.method == 'POST':
			fileCsv = request.files['file']
			csvfile = fileCsv
			reader = csv.DictReader( csvfile)
			

			jsonData = []

			for row in reader:
				jsonData.append(row)

			# print jsonData

			quiz = Quiz()
			quiz.quizName = fileCsv.filename
			quiz.creatorId = current_user.get_id()
			quiz.questionsIdList = jsonData

			db.session.add(quiz)
			db.session.commit()

			token = quiz.generateToken()

			return redirect(url_for('quiz.view', token = token))

		else:
			return render_template('quiz/upload.html')
		# then only allow these actions to occur
		# get questions from excel file
		# create unique form with these questions
	else:
		flash('You are not allowed to create quizzes')
		return redirect(url_for('main.index'))