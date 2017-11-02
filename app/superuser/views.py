from flask import render_template, redirect, request, url_for, flash
from . import superuser
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User, Request, Role
# from .forms import LoginForm, RegistrationForm
from ..email import send_email
from app import db
from .forms import UpgradeForm

@superuser.route('/upgrade/', methods=['GET', 'POST'])
@login_required
def upgrade():
	form = UpgradeForm()

	if form.validate_on_submit():
		# send email and add request row
		if form.upgradeToCreater.data:
			requestUpgrade = Request()
			requestUpgrade.role_id = Role.query.filter_by(permissions = 2).first()
			requestUpgrade.user_id = current_user.get_id()
			requestUpgrade.status = 0

			db.session.add(requestUpgrade)

			return redirect(url_for('main.index'))
		elif form.upgradeToSuperUser.data:
			requestUpgrade = Request()
			requestUpgrade.role_id = Role.query.filter_by(permissions = 4).first()
			requestUpgrade.user_id = current_user.get_id()
			requestUpgrade.status = 0

			db.session.add(requestUpgrade)

			return redirect(url_for('main.index'))

	else:
		# get possible request row entry and render form
		# requests = Request.query.filter_by(user_id = current_user.get_id())
		# creatorRequest = requests.filter_by(role_id = Role.query.filter_by(permissions = 2).first().id).first()
		# if creatorRequest:
		# 	if creatorRequest.status == 0:
		# 		form.upgradeToCreater.label = 'Request sent'
		# 		form.upgradeToCreater.id = 'disabledButton'

		# 	elif creatorRequest.status == 1:
		# 		form.upgradeToCreater.label = 'Request accepted'
		# 		form.upgradeToCreater.id = 'disabledButton'

		# 	elif creatorRequest.status == 2:
		# 		form.upgradeToCreater.label = 'Request declined'
		# 		form.upgradeToCreater.id = 'disabledButton'
		
		# else:
		# 	form.upgradeToCreater.label = 'Upgrade to Quiz creator'
		# 	form.upgradeToCreater.id = 'enabledButton'

		# superUserRequest = requests.filter_by(role_id = Role.query.filter_by(permissions = 4).first().id).first()
		# if superUserRequest:
		# 	if superUserRequest.status == 0:
		# 		form.upgradeToSuperUser.label = 'Request sent'
		# 		form.upgradeToSuperUser.id = 'disabledButton'

		# 	elif superUserRequest.status == 1:
		# 		form.upgradeToSuperUser.label = 'Request accepted'
		# 		form.upgradeToSuperUser.id = 'disabledButton'

		# 	elif superUserRequest.status == 2:
		# 		form.upgradeToSuperUser.label = 'Request declined'
		# 		form.upgradeToSuperUser.id = 'disabledButton'

		# else:
		# 	form.upgradeToSuperUser.label = 'Upgrade to Super User'
		# 	form.upgradeToSuperUser.id = 'enabledButton'
			
		return render_template('superuser/requestUpgrade.html', form = form)

			# elif creatorRequest.first().status == 1:
			# 	form.upgradeToCreater.
			# means request for quiz creator has been sent