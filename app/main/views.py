from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Score, Quiz
from ..email import send_email
from . import main
from .forms import NameForm
from flask_login import current_user
from ..quiz.views import QUESTIONSCORE

@main.route('/')
def index():
    if current_user.is_authenticated:
        role_id = User.query.filter_by(id=current_user.get_id()).first().role_id
    else:
    	return render_template('index.html')

    if role_id == -1:
    	pass
    elif role_id == 1:
    	# get all submitted quizzes
    	scores = Score.query.filter_by(giverId = current_user.get_id())
    	
    	quizNamesList = []
    	scoresList = []
    	totalScoresList = []
    	tokensList = []

    	for score in scores:
    		quiz = Quiz.query.filter_by(id = score.quizId).first()
    		totalScoresList.append( len( quiz.questionsIdList ) * QUESTIONSCORE )
    		quizNamesList.append(quiz.quizName)
    		scoresList.append(score.score)
    		totalScoresList.append
    		tokensList.append(quiz.generateToken())

    	listLen = len(quizNamesList)
    	return render_template('quizTaker.html', quizNamesList = quizNamesList, scoresList = scoresList, tokensList = tokensList, listLen = listLen, totalScoresList = totalScoresList, user= current_user)

    elif role_id == 2 or role_id == 3:
    	quizzes = Quiz.query.filter_by(creatorId = current_user.get_id())
    	quizNamesList = []
    	quizTokenList = []

    	for quiz in quizzes:
    		quizNamesList.append(quiz.quizName)
    		quizTokenList.append(quiz.generateToken())

    	listLen = len(quizTokenList)

    	if role_id == 2:
    		role = "Quiz Setter"
    	else: 
    		role = "Super User"

    	return render_template('quizSetter.html', user = current_user, quizTokenList = quizTokenList, quizNamesList = quizNamesList, listLen = listLen, role = role)
