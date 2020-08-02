from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,SelectField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):

	name=StringField("Employee Name:",validators=[DataRequired()])
	project=StringField("Project Name:")
	em_no=StringField("Employee No:",validators=[DataRequired()])
	hackrankid=StringField("Hacker Rank ID:",validators=[DataRequired()])
	cert=StringField("Certifications:")
	skill=StringField("Skills:")
	badge=StringField("Badges:")
	n_s=IntegerField("No of Stars:")
	c_s=SelectField('Contest/Practice:',choices=[('contest','Contest'),('practice','Practice')])
	submit=SubmitField('Add Employee')

class DelForm(FlaskForm):

	id=IntegerField("Enter the ID of the employee to be delete:",validators=[DataRequired()])
	submit=SubmitField("Delete Employee")
