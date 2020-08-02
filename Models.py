import os

from forms import AddForm,DelForm

from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'

######################################################
################ SQL DATABASE SECTION ################
######################################################

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)
Migrate(app,db)

class Hacker_Rank(db.Model):
	__tablename__='Hacker Rank'
	id=db.Column(db.Integer,primary_key=True)
	project=db.Column(db.Text)
	e_num=db.Column(db.Text)
	e_name=db.Column(db.Text)
	hr_userid=db.Column(db.Text)
	cert=db.Column(db.Text)
	skill=db.Column(db.Text)
	badges=db.Column(db.Text)
	n_stars=db.Column(db.Integer)
	c_p=db.Column(db.Text)

	def __init__(self,project,e_num,e_name,hr_userid,cert,skill,badges,n_stars,c_p):
		self.project=project
		self.e_num=e_num
		self.e_name=e_name
		self.hr_userid=hr_userid
		self.cert=cert
		self.skill=skill
		self.badges=badges
		self.n_stars=n_stars
		self.c_p=c_p

	def __repr__(self):
		return f"\nEmployee Name: {self.e_name} \n<br>Employee ID: {self.e_num} \nProject: {self.project}\nHacker Rank Id: {self.hr_userid}\nCertificates: {self.cert}\nSkillset: {self.skill}\nBadges: {self.badges}\nNo of Stars: {self.n_stars}\nContest/Practice: {self.c_p}"

class Shrishti(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	date_pre=db.Column(db.Text)
	project=db.Column(db.Text)
	e_num=db.Column(db.Text)
	presenter=db.Column(db.Text)
	topic=db.Column(db.Text)

	def __init__(self,date_pre,project,e_num,presenter,topic):
		self.date_pre=date_pre
		self.project=project
		self.e_num=e_num
		self.presenter=presenter
		self.topic=topic

	def __repr__(self):
		return f"\nDate of Presentation: {self.date_pre}\nProject: {self.project}\nEmployee No: {self.e_num}\nPresenter: {self.presenter}\nTopic: {self.topic}"

class Pragati(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	project=db.Column(db.Text)
	em_num=db.Column(db.Text)
	em_name=db.Column(db.Text)
	no_sub=db.Column(db.Integer)

	def __init__(self,project,em_no,em_name,no_sub):
		self.project=project
		self.em_num=em_no
		self.em_name=em_name
		self.no_sub=no_sub

	def __repr__(self):
		return f"\nProject: {self.project}\n<br>Employee No: {self.em_num}\nEmployeeName: {self.em_name}\nNo of Submission: {self.no_sub}"


#######################################################
########### VIEW FUNCTIONS -- HAVE FORMS ##############
#######################################################

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/add',methods=['GET','POST'])
def add():

	form=AddForm()

	if form.validate_on_submit():
		name=form.name.data
		project=form.project.data
		em_no=form.em_no.data
		hackrankid=form.hackrankid.data
		cert=form.cert.data
		skill=form.skill.data
		badge=form.badge.data
		n_s=form.n_s.data
		c_s=form.c_s.data

		new_emp=Hacker_Rank(project,em_no,name,hackrankid,cert,skill,badge,n_s,c_s)
		db.session.add(new_emp)
		db.session.commit()

		return redirect(url_for('list'))
		
	return render_template('add.html',form=form)

@app.route('/list')
def list():
	emp=Hacker_Rank.query.all()
	return render_template('list.html',emp=emp)


@app.route('/delete',methods=['GET','POST'])
def delete():

	form=DelForm()

	if form.validate_on_submit():
		try:
			empid=form.id.data
			emp=Hacker_Rank.query.filter_by(e_num=empid)
			db.session.delete(emp[0])
			db.session.commit()
		except IndexError:
			pass
		

		return redirect(url_for('list'))

	return render_template('delete.html',form=form)


if __name__=='__main__':
	app.run(debug=True)

