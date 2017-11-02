from flask import render_template, redirect, request, url_for, flash
from . import superuser
# from flask_login import login_required, login_user, logout_user, current_user
from ..models import User, Request
# from .forms import LoginForm, RegistrationForm
from ..email import send_email
from app import db
from .form import UpgradeForm

@superuser.route('/upgrade/', methods=['GET', 'POST'])
@login_required
def upgrade():
	form = UpgradeForm()

	if form.validate_on_submit():
		# send email and add request row
		if form.upgradeToCreater.data:
			requestUpgrade = Request()
			
	else:
		# get possible request row entry and render form