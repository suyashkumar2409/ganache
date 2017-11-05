from flask import render_template, redirect, request, url_for, flash
from . import quiz
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from ..email import send_email
from app import db

@quiz.route('/create', methods = ['GET', 'POST'])
@login_required
def createQuiz():
	if current_user.role_id == 2 or current_user.role_id == 4:
		# then only allow these actions to occur
		# get questions from excel file
		# create unique form with these questions
	else:
		flash('You are not allowed to create quizzes')
		return redirect(url_for('main.index'))