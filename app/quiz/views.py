from flask import render_template, redirect, request, url_for, flash, jsonify
from . import quiz
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User, Quiz
# from .forms import LoginForm, RegistrationForm
from ..email import send_email
from app import db
import csv
import json

@quiz.route('/view/<token>')
@login_required
def view(token):
	if request.method == 'POST':
		# analyse answers here
		pass
	else:
		# render quiz here
		quizId = token.split('-')[0]
		print quizId
		print token
		isCreator = False
		quiz = Quiz.query.filter_by(id = quizId).first()

		if quiz is not None:
			quizName = quiz.quizName
			creatorId = quiz.creatorId

			if creatorId == current_user.get_id():
				isCreator = True
			else:
				isCreator = False

			questions = list(quiz.questionsIdList)
			print questions

			# return redirect(url_for('main.index'))
			
			return render_template('quiz/quiz.html', isCreator = isCreator, quizName = quizName, questions = questions, token = token)


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

			print jsonData

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