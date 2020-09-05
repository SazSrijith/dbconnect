from __init__ import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

class User(db.Model,UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	pass_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean)
	emp_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))

	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self.pass_hash = generate_password_hash(password=password)
		self.is_admin = False

	def make_admin(self):
		self.is_admin = True

	def add_empid(self, empid):
		self.emp_id = empid

	def check_password(self, password):
		return check_password_hash(self.pass_hash, password)



class Employee(db.Model):
	__tablename__='employee'
	employee_id=db.Column(db.Integer,primary_key=True)
	employee_first_name=db.Column(db.Text)
	employee_last_name=db.Column(db.Text)
	employee_hacker_rank_id=db.Column(db.Text, unique=True)
	# employees = db.relationship('Project', secondary=proemp, backref=db.backref('projectemp', lazy='dynamic'))
	emppro_id=db.Column(db.Integer, db.ForeignKey('project.project_id'))
	scores = db.relationship('Score', backref='empsc')
	userid = db.relationship('User', backref='empid')

	def __init__(self,employee_id,employee_first_name,employee_last_name,employee_hacker_rank_id,emppro=None):
		self.employee_id=employee_id
		self.employee_first_name=employee_first_name
		self.employee_last_name=employee_last_name
		self.employee_hacker_rank_id=employee_hacker_rank_id
		self.emppro = emppro

	def __repr__(self):
		return f"\nEmployee ID: {self.employee_id}\nEmployee Name: {self.employee_first_name} {self.employee_last_name}\nEmployee Hacker Rank ID: {self.employee_hacker_rank_id}"


class Project(db.Model):
	__tablename__ = 'project'
	project_id = db.Column(db.Integer, primary_key=True)
	project_name = db.Column(db.Text)
	project_start_date = db.Column(db.Text)
	project_end_date = db.Column(db.Text)
	employees= db.relationship('Employee',backref='emppro')

	def __init__(self, project_id, project_name, project_start_date, project_end_date):
		self.project_id = project_id
		self.project_name = project_name
		self.project_start_date = project_start_date
		self.project_end_date = project_end_date

	def __repr__(self):
		return f"\nProject ID: {self.project_id} \nProject Name: {self.project_name} \nProject Start Date: {self.project_start_date}\nProject End Date: {self.project_end_date}"

class Skill(db.Model):
	__tablename__ = 'skill'
	id = db.Column(db.Integer, primary_key=True)
	skill_name = db.Column(db.Text)
	scores = db.relationship('Score', backref='skillsc')

	def __init__(self, skill_name):
		self.skill_name = skill_name

class Score(db.Model):
	__tablename__ = 'score'
	id = db.Column(db.Integer, primary_key=True)
	month = db.Column(db.Text)
	score = db.Column(db.Integer)
	badge = db.Column(db.Text)
	no_of_stars = db.Column(db.Text)
	empsc_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
	skillsc_id = db.Column(db.Integer, db.ForeignKey('skill.id'))

	def __init__(self, month, score, badge, no_of_stars):
		self.month = month
		self.score = score
		self.badge = badge
		self.no_of_stars = no_of_stars


# class ProjectEmployee(db.Model):
# 	id=db.Column(db.Integer,primary_key=True)
# 	project_id=db.Column(db.Integer,db.ForeignKey(ProjectMaster.project_id))
# 	employee_id=db.Column(db.Integer,db.ForeignKey(EmployeeMaster.employee_id))
#
# 	def __init__(self,project_id,employee_id):
# 		self.project_id=project_id
# 		self.employee_id=employee_id
#
# 	def __repr__(self):
# 		return f"\nProject ID: {self.project_id}\nEmployee ID: {self.employee_id}"



# class SkillMaster(db.Model):
# 	skill_id = db.Column(db.Text,primary_key=True)
# 	skill_name = db.Column(db.Text)
#
# 	def __init__(self,skill_id,skill_name):
# 		self.skill_id=skill_id
# 		self.skill_name=skill_name
#
# 	def __repr__(self):
# 		return f"\nSkill ID: {self.skill_id}\nSkill Name: {self.skill_name}"
#
#
# class Certification(db.Model):
# 	id=db.Column(db.Integer,primary_key=True)
# 	employee_id = db.Column(db.Integer,db.ForeignKey('EmployeeMaster.employee_id'))
# 	skill_id = db.Column(db.Integer,db.ForeignKey('SkillMaster.skill_id'))
# 	certification_name=db.Column(db.Text)
#
#
# 	def __init__(self,skill_id,employee_id,certification_name):
# 		self.skill_id=skill_id
# 		self.employee_id=employee_id
# 		self.certification_name=certification_name
#
# 	def __repr__(self):
# 		return f"\nEmployee ID: {self.employee_id}\nSkill ID: {self.skill_id}\nCertification Name: {self.certification_name}"
#
# class Scores(db.Model):
# 	id=db.Column(db.Integer,primary_key=True)
# 	employee_id = db.Column(db.Integer,db.ForeignKey('EmployeeMaster.employee_id'))
# 	skill_id = db.Column(db.Integer,db.ForeignKey('SkillMaster.skill_id'))
# 	month=db.Column(db.Text)
# 	score=db.Column(db.Integer)
# 	badge=db.Column(db.Text)
# 	no_of_stars=db.Column(db.Integer)
#
#
# 	def __init__(self,employee_id,skill_id,month,score,badges,no_of_stars):
# 		self.employee_id=employee_id
# 		self.skill_id=s_id
# 		self.month=month
# 		self.score=score
# 		self.badges=badges
# 		self.no_of_stars=no_of_stars
#
# 	def __repr__(self):
# 		return f"\nEmployee ID: {self.employee_id}\nSkill ID: {self.skill_id} \nMonth: {self.month}\nScore: {self.score}\nBadge: {self.badge}\nNo of Stars: {self.no_of_stars}"
