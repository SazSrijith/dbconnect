from forms import AddEmployee,AddProject,AssignProject,SearchEmployee,SearchProject,AddSkill,AddScore,LoginForm,SignUpForm,MakeAdmin,ChartForm
from __init__ import app,db
from models import  Project,Employee,Skill,Score,User
from flask import Flask,render_template,url_for,redirect,request,flash,abort,session
from flask_login import login_user,login_required,logout_user
import pandas as pd
from sqlalchemy.exc import IntegrityError

# Home Page

@app.route('/')
def home():
	return render_template('home.html')

# LogOut

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out ! ')
    return redirect(url_for('home'))

# LogIn

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            if user.check_password(form.password.data) :
                login_user(user)

                if user.is_admin:
                    session['is_admin']=True
                else:
                    rec=Employee.query.filter_by(employee_id=user.emp_id).first()
                    session['emp_name'] = rec.employee_first_name + " " + rec.employee_last_name
                    session['emp_no']=user.emp_id
                    session['is_admin']=False
                flash("Logged in successfully")
                return redirect(url_for('home'))
            flash("Wrong email Id or Password!")
            return render_template('login.html', form=form)
        flash("Wrong email Id or Password!")
        return render_template('login.html', form=form)
    return render_template('login.html',form=form)

# SignUp

@app.route('/signup',methods=['GET','POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		new_user = User(
			email = form.email.data,
			username = form.username.data,
			password = form.password.data)
		if form.employee_id.data:
			employee_id = form.employee_id.data
			employee_first_name = form.employee_first_name.data
			employee_last_name = form.employee_last_name.data
			employee_hacker_rank_id = form.employee_hacker_rank_id.data
			new_emp = Employee(employee_id, employee_first_name, employee_last_name, employee_hacker_rank_id)
			new_user.add_empid(form.employee_id.data)
			db.session.add_all([new_emp,new_user])
			try:
				db.session.commit()
				flash("You have successfully been registered!")
				return redirect(url_for('home'))
			except IntegrityError:
				db.session.rollback()
				if str(ex.args).find('email') != -1:
					flash("This Email has already been registerd!")
				elif str(ex.args).find('username') != -1:
					flash("This Username is already taken!")
				elif str(ex.args).find('employee_id') != -1:
					flash("Employee with the same Employee ID already Exists!")
				elif str(ex.args).find('employee_hacker_rank_id') != -1:
					flash("Employee with the same Hacker Rank ID already Exists!")
				else:
					pass
				return render_template('signup.html', form=form)
	return render_template('signup.html',form=form)

# To Add a Employee to the Database

@app.route('/addemployee',methods=['GET','POST'])
@login_required
def add_employee():
	if session['is_admin']:
		form=AddEmployee()
		if form.validate_on_submit():
			employee_id=form.employee_id.data
			employee_first_name=form.employee_first_name.data
			employee_last_name=form.employee_last_name.data
			employee_hacker_rank_id=form.employee_hacker_rank_id.data
			new_emp=Employee(employee_id,employee_first_name,employee_last_name,employee_hacker_rank_id)
			db.session.add(new_emp)
			try:
				db.session.commit()
				return redirect(url_for('list_employee'))
			except IntegrityError:
				flash("Employee with the same Employee ID or Hacker Rank ID  already Exists")
				db.session.rollback()
				return render_template('employee/addEmployee.html', form=form)
		return render_template('employee/addEmployee.html',form=form)
	else:
		abort(404, description="You dont have access to this URL.")

# To Add a Project to the Database

@app.route('/addproject',methods=['GET','POST'])
@login_required
def add_project():
	if session['is_admin']:
		form=AddProject()
		if form.validate():
			project_id=form.project_id.data
			project_name=form.project_name.data
			project_start_date=form.project_start_date.data.strftime('%d/%m/%Y')
			project_end_date=form.project_end_date.data.strftime('%d/%m/%Y')
			new_pro=Project(project_id,project_name,project_start_date,project_end_date)
			db.session.add(new_pro)
			try:
				db.session.commit()
				return redirect(url_for('list_project'))
			except IntegrityError:
				flash("Project with the same Project ID already Exists")
				db.session.rollback()
				return render_template('project/addProject.html',form=form)
		return render_template('project/addProject.html',form=form)
	else:
		abort(404, description="You dont have access to this URL.")

# To Add a skill to the Database

@app.route('/addskill',methods=['GET','POST'])
@login_required
def add_skill():
	if session['is_admin']:
		form=AddSkill()
		if form.validate_on_submit():
			skill_name=form.skill_name.data
			new_skill=Skill(skill_name)
			db.session.add(new_skill)
			db.session.commit()
			return redirect(url_for('list_skill'))
		return render_template('skill/addSkill.html',form=form)
	else:
		abort(404, description="You dont have access to this URL.")

# To List all the Employees in the Database

@app.route('/listemployee')
@login_required
def list_employee():
	if session['is_admin']:
		emp=Employee.query.all()
		empprodict = []
		if emp:
			for e in emp:
				pro = Project.query.filter_by(project_id=e.emppro_id).first()
				case = {'e no': e.employee_id, 'e name': e.employee_first_name + " " + e.employee_last_name,
						'hack id': e.employee_hacker_rank_id}
				if pro:
					case['p name'] = pro.project_name
				else:
					case['p name'] = 'Not Assigned'
				empprodict.append(case)
			return render_template('employee/listEmployee.html', empprodict=empprodict)
		return render_template('employee/listEmployee.html',emp=emp)
	else:
		abort(404, description="You dont have access to this URL.")
# To List all the Projects in the Database

@app.route('/listproject')
@login_required
def list_project():
	if session['is_admin']:
		pro=Project.query.all()
		return render_template('project/listProject.html',pro=pro)
	else:
		abort(404, description="You dont have access to this URL.")

# To List all the Skills in the Database

@app.route('/listskill')
@login_required
def list_skill():
	skill=Skill.query.all()
	return render_template('skill/listSkill.html',skill=skill)


# To ASSIGN a PROJECT to an EMPLOYEE

@app.route('/assignproject',methods=['GET','POST'])
@login_required
def assign_project():
	if session['is_admin']:
		form=AssignProject()
		form.employee.choices = [(emp.employee_id,emp.employee_first_name)for emp in Employee.query.all()]
		form.project.choices = [(pro.project_id, pro.project_name) for pro in Project.query.all()]
		if form.is_submitted():
			employee_id = form.employee.data
			project_id = form.project.data
			emp=Employee.query.filter_by(employee_id=employee_id).first()
			# pro=Project.query.filter_by(project_id=project_id).first()
			emp.emppro_id=project_id
			db.session.add(emp)
			db.session.commit()
			return redirect(url_for('list_employee'))
		return render_template('employee/assignProject.html',form=form)
	else:
		abort(404, description="You dont have access to this URL.")

# To Find a Record in the Database

@app.route('/search_record/<no>',methods=['GET', 'POST'])
@login_required
def search_record(no):
	if session['is_admin']:
		if no =='0' or no == '2' or no =='4':
			form=SearchEmployee()
			form.emp_id.choices =  [(emp.employee_id,str(emp.employee_id)+" - "+emp.employee_first_name+" "+emp.employee_last_name)for emp in Employee.query.all()]
			if form.is_submitted():
				recid = form.emp_id.data
				if no =='0':
					return redirect(url_for('delete', recid=recid,item='employee'))
				elif no == '2' :
					return redirect(url_for('modify', recid=recid, item='employee'))
				else :
					return redirect(url_for('e_profile', recid=recid))
			return render_template('searchRecord.html',form=form,no=no)
		else :
			form = SearchProject()
			form.pro_id.choices = [(pro.project_id, pro.project_name) for pro in Project.query.all()]
			if form.is_submitted():
				recid = form.pro_id.data
				if no == '1':
					return redirect(url_for('delete', recid=recid, item='project'))
				else :
					return redirect(url_for('modify', recid=recid, item='project'))
			return render_template('searchRecord.html',form=form, no=no)
	else:
		abort(404, description="You dont have access to this URL.")
# To Delete an Employee or Project

@app.route('/delete/<recid>/<item>')
@login_required
def delete(recid,item):
	if session['is_admin']:
		if(item == 'employee'):
			rec=Employee.query.filter_by(employee_id=recid).first()
			score=Score.query.filter_by(empsc_id=recid).all()
			if rec:
				for sc in score:
					db.session.delete(sc)
				db.session.delete(rec)
				db.session.commit()
				return redirect(url_for('list_employee'))
		elif (item == 'project'):
			rec=Project.query.filter_by(project_id=recid).first()
			if rec:
				db.session.delete(rec)
				db.session.commit()
				return redirect(url_for('list_project'))
		return render_template('home.html')
	else:
		abort(404, description="You dont have access to this URL.")

# To Modify the details of an Employee or a Project

@app.route('/modify/<recid>/<item>',methods=['GET','POST'])
@login_required
def modify(recid,item):
	if session['is_admin']:
		if (item == 'employee'):
			print("yES")
			rec=Employee.query.filter_by(employee_id=recid).first()
			if rec:
				print("yES IN REC")
				form=AddEmployee()
				if form.is_submitted():
					print("VALIDATE SUCCESS")
					rec.employee_first_name = form.employee_first_name.data
					rec.employee_last_name = form.employee_last_name.data
					rec.employee_hacker_rank_id = form.employee_hacker_rank_id.data
					db.session.add(rec)
					db.session.commit()
					return redirect(url_for('list_employee'))
				return render_template('employee/modifyEmployee.html',form=form,rec=rec)
			else:
				return redirect(url_for('search_record', no=2))
		else:
			rec = Project.query.filter_by(project_id=recid).first()
			if rec:
				form = AddProject()
				if form.validate_on_submit():
					rec.project_id = form.project_id.data
					rec.project_name = form.project_name.data
					rec.project_start_date = form.project_start_date.data
					rec.project_end_date = form.project_end_date.data
					db.session.add(rec)
					db.session.commit()
					return redirect(url_for('list_project'))
				return render_template('project/modifyProject.html', form=form, rec=rec)
			else:
				return redirect(url_for('search_record', no=2))
	else:
		abort(404, description="You dont have access to this URL.")

# To Add a Score to the Scoreboard

@app.route('/addscore',methods=['GET','POST'])
@login_required
def add_score():
	form=AddScore()
	if session['is_admin']:
		form.employee.choices = [(emp.employee_id, emp.employee_first_name) for emp in Employee.query.all()]
	else:
		form.employee.choices = [(session['emp_no'], session['emp_name'])]
	form.skill.choices = [(skill.id, skill.skill_name) for skill in Skill.query.all()]
	if form.is_submitted():
		dup_flag=False
		empsc_id = form.employee.data
		month = form.month.data
		score = form.score.data
		skillsc_id = form.skill.data
		if score<100:
			badge ='Bronze'
			no_of_stars=2
		elif score>100 and score<200:
			badge = 'Silver'
			no_of_stars=3
		else:
			badge='Gold'
			no_of_stars=4
		emp=Score.query.filter_by(empsc_id=empsc_id).all()
		for e in emp:
			if e.skillsc_id == int(skillsc_id) and (e.month==month):
				dup_flag=True
		if not dup_flag:
			print(dup_flag)
			new_score=Score(month,score,badge,no_of_stars)
			new_score.empsc_id=empsc_id
			new_score.skillsc_id=skillsc_id
			db.session.add(new_score)
			db.session.commit()
			if session['is_admin']:
				return redirect(url_for('list_scoreboard'))
			else:
				return redirect(url_for('e_profile',recid=session['emp_no']))
		else:
			flash("This Employee has already got a Score for the below mentioned Month and Skill!")
			return render_template('score/addScore.html',form=form)
	return render_template('score/addScore.html',form=form)


# To Display the Scoreboard

@app.route('/listscoreboard',methods=['GET','POST'])
@login_required
def list_scoreboard():
	if session['is_admin']:
		score=Score.query.all()
		scoreboard = []
		if score:
			for sc in score:
				emp = Employee.query.filter_by(employee_id=sc.empsc_id).first()
				pro = Project.query.filter_by(project_id=emp.emppro_id).first()
				skill = Skill.query.filter_by(id=sc.skillsc_id).first()
				case = {'month': sc.month, 'badge': sc.badge,
						'score': sc.score, 'no_of_star':sc.no_of_stars,'emp name':emp.employee_first_name+" "+emp.employee_last_name,'skill name':skill.skill_name}
				if pro:
					case['p name'] = pro.project_name
				else:
					case['p name'] = 'Not Assigned'
				scoreboard.append(case)
			return render_template('score/listScoreboard.html',scoreboard=scoreboard)
		return render_template('score/listScoreboard.html',score=score)
	else:
		abort(404, description="You dont have access to this URL.")

# To display the Employee Profile

@app.route('/e_profile/<recid>')
@login_required
def e_profile(recid):
	if str(session['emp_no'])==recid or  session['is_admin']:
		found=False
		emp = Employee.query.filter_by(employee_id=recid).first()
		e_info ={
			'e no': emp.employee_id,
			'e name': emp.employee_first_name+" "+emp.employee_last_name,
			'hack id': emp.employee_hacker_rank_id
		}
		pro = Project.query.filter_by(project_id=emp.emppro_id).first()
		if pro:
			e_info['p name'] = pro.project_name
		else:
			e_info['p name'] = 'Not Assigned'
		score = Score.query.filter_by(empsc_id=emp.employee_id).all()
		e_skills=[]
		if score:
			found=True
			score_list=[]
			for sc in score:
				skill=Skill.query.filter_by(id=sc.skillsc_id).first()
				case = {'month': sc.month, 'skill': skill.skill_name, 'badge': sc.badge, 'no_of_stars': sc.no_of_stars,
						'score': sc.score}
				score_list.append(case)
				if skill.skill_name not in e_skills:
					e_skills.append(skill.skill_name)
		return render_template('employee/employeeProfile.html',e_info=e_info,e_skills=e_skills,score=score_list)
	else:
		abort(404, description="You dont have access to this URL.")

# To generate a Chart

@app.route('/chart/',methods=['GET','POST'])
def chart():
	empname = []
	empscores= []
	months=[]
	skills = []
	form = ChartForm()

	scores = Score.query.all()
	for score in scores:
		eskill = Skill.query.filter_by(id=score.skillsc_id).first()
		if score.month not in months:
			months.append(score.month)
		if eskill.skill_name not in skills:
			skills.append(eskill.skill_name)

	form.skill.choices=[("","")]
	form.month.choices=[("","")]
	for skill in skills:

		form.skill.choices.append((skill,skill))
	for month in months:
		form.month.choices.append((month,month))

	for score in scores:
		ename = Employee.query.filter_by(employee_id=score.empsc_id).first()
		name = ename.employee_first_name + " " + ename.employee_last_name
		empname.append(name)
		empscores.append(score.score)
	if form.is_submitted():
		empname_fb_skill = []
		empscores_fb_skill = []
		empname_fb_month = []
		empscores_fb_month = []
		record_fb_skill=[]
		record_fb_month=[]
		empname = []
		empscores = []

		if form.skill.data:
			eskill = Skill.query.filter_by(skill_name=form.skill.data).first()
			score_fb_skill = Score.query.filter_by(skillsc_id=int(eskill.id)).all()
			for score in score_fb_skill:
				ename = Employee.query.filter_by(employee_id=score.empsc_id).first()
				name = ename.employee_first_name + " " + ename.employee_last_name
				case = {'id': score.id, 'name': name, 'score': score.score}
				name = name+"("+score.month+")"
				empname_fb_skill.append(name)
				empscores_fb_skill.append(score.score)
				record_fb_skill.append(case)

		if form.month.data:
			score_fb_month = Score.query.filter_by(month=form.month.data).all()
			for score in score_fb_month:
				eskill = Skill.query.filter_by(id=score.skillsc_id).first()
				ename = Employee.query.filter_by(employee_id=score.empsc_id).first()
				name = ename.employee_first_name + " " + ename.employee_last_name
				case = {'id': score.id, 'name': name, 'score': score.score}
				name = name + "("+eskill.skill_name+")"
				empname_fb_month.append(name)
				empscores_fb_month.append(score.score)

				record_fb_month.append(case)

		if form.skill.data and form.month.data:
			for (rec_skill) in record_fb_skill:
				for rec_month in record_fb_month:
					if rec_skill['id'] == rec_month['id']:
						empname.append(rec_skill['name'])
						empscores.append(rec_skill['score'])
			if not empname:
				flash("No data found for the given skill and month!")
		elif form.skill.data:
			empname = empname_fb_skill
			empscores = empscores_fb_skill
		elif form.month.data:
			empname = empname_fb_month
			empscores = empscores_fb_month
		else:
			scores = Score.query.all()
			for score in scores:
				eskill = Skill.query.filter_by(id=score.skillsc_id).first()
				ename = Employee.query.filter_by(employee_id=score.empsc_id).first()
				name = ename.employee_first_name + " " + ename.employee_last_name+"("+score.month+") "+ "("+eskill.skill_name+")"
				empname.append(name)
				empscores.append(score.score)
	return render_template('chart.html', emp_name=empname, score=empscores, form=form)

	# # if skill_id != '0':
	# # 	scores = Score.query.filter_by(skillsc_id=int(skill_id)).all()
	# # 	skill = Skill.query.filter_by(id=int(skill_id)).first()
	# # 	sname=skill.skill_name
	# # 	for score in scores:
	# # 		ename = Employee.query.filter_by(employee_id=score.empsc_id).first()
	# # 		month = score.month
	# # 		name_and_month=ename.employee_first_name + " " + ename.employee_last_name + "("+month+")"
	# # 		empname.append(name_and_month)
	# # 		empscores.append(score.score)
	#
	# return render_template('chart.html',emp_name=empname,score=empscores,form=form)








@app.route('/download_table')
def download_table():
	url = "http://127.0.0.1:5000/listemployee"
	table = pd.read_html(url)
	for t in table:
		print(t)
	# table.to_excel("downloads/datascore.xlsx",index=False)
	return redirect(url_for('list_employee'))

#



db.create_all()
if __name__=='__main__':
	app.run(debug=True)

