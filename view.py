from forms import AddForm,SearchForm
from models import Hacker_Rank,Shrishti,Pragati,db,app
from flask import Flask,render_template,url_for,redirect
from flask_migrate import Migrate

Migrate(app,db)

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


@app.route('/delete/<empid>',methods=['GET','POST'])
def delete(empid):
	try:
		emp=Hacker_Rank.query.filter_by(e_num=empid)
		db.session.delete(emp[0])
		db.session.commit()
	except IndexError:
		pass
	return redirect(url_for('list'))


@app.route('/search/<no>',methods=['GET','POST'])
def search(no):
	form=SearchForm()
	if form.validate_on_submit():
		try:
			empid=form.id.data
			form=AddForm()
			print(type(no))
			if(no=="0"):
				return redirect(url_for('update',empid=empid))
			else:
				return redirect(url_for('delete',empid=empid))
		except IndexError:
				pass
	return render_template('search.html',form=form,no=no)

@app.route('/update/<empid>',methods=['GET','POST'])
def update(empid):
	try:
		form=AddForm()
		emp=Hacker_Rank.query.filter_by(e_num=empid)
		em=emp[0]
	except IndexError:
		return redirect(url_for('search',no=0))

	if form.validate_on_submit():
		em.e_name=form.name.data
		em.project=form.project.data
		em.e_num=form.em_no.data
		em.hr_userid=form.hackrankid.data
		em.cert=form.cert.data
		em.skill=form.skill.data
		em.badges=form.badge.data
		em.n_stars=form.n_s.data
		em.c_p=form.c_s.data
		db.session.add(em)
		db.session.commit()
		return redirect(url_for('list'))
	return render_template('update.html',form=form,em=em)

if __name__=='__main__':
	app.run(debug=True)

