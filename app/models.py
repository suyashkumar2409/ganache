from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer, index = True)

    requests = db.relationship('Request', backref='roleRequestList', lazy = 'dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key = True)
    giverId = db.Column(db.Integer, db.ForeignKey('users.id'), default = 1, index = True)
    quizId = db.Column(db.Integer, db.ForeignKey('quizzes.id'), default = 1, index = True)
    score = db.Column(db.Integer)
    answers  = db.Column(db.PickleType)


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key = True)
    quizName = db.Column(db.String(128), default = '')
    creatorId = db.Column(db.Integer, db.ForeignKey('users.id'), default = 1)
    questionsIdList = db.Column(db.PickleType)

    questions = db.relationship('Question', backref='questionList', lazy = 'dynamic')
    # array of questions id
    # fk to creator -- done
    # unique link -- done
    def generateToken(self):
        return str(self.id) + '-' + str(self.quizName)

    def getShareableLink(self):
        return url_for('quiz.give', token = self.generateToken(), _external = True)

    def __repr__(self):
        return '<Role %r>' % self.quizName

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), default = 1)
    questionName = db.Column(db.String(512))
    opt1 = db.Column(db.String(128))
    opt2 = db.Column(db.String(128))
    opt3 = db.Column(db.String(128))
    opt4 = db.Column(db.String(128))
    correctAns = db.Column(db.String(128))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default = 1)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default = False)

    requests = db.relationship('Request', backref='userRequestList', lazy = 'dynamic')
    quizList = db.relationship('Quiz', backref='quizList', lazy = 'dynamic')
    scores = db.relationship('Score', backref='scoresList', lazy = 'dynamic')


    def generate_confirmation_token(self, expiration = 60*60*48):
    	s = Serializer(current_app.config['SECRET_KEY'], expiration)
    	return s.dumps({'confirm':self.id})

    def generate_token_role(self, expiration = 60*60*48, role = 2, requestId = -1):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id, 'role':role, 'requestId':requestId})

    def confirm(self, token):
    	s = Serializer(current_app.config['SECRET_KEY'])
    	try:
    		data = s.loads(token)
    	except:
            print('loads didnt work')
            return False
    	if data.get('confirm') != self.id:
            print(data.get('confirm'))
            print(self.id)
            return False

        self.confirmed = True
        db.session.add(self)
        return True

 	   	
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Request(db.Model):
    __tablename__ = 'requests'

    request_id = db.Column(db.Integer, primary_key = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index = True)
    status = db.Column(db.Integer)
    # status - 0, sent, 1, accepted, 2 declined
class Permission:
    ATTEMPT = 0x01
    CREATE = 0x02
    SHUTDOWN = 0x04