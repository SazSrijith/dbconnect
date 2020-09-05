from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, FileField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo , Regexp


class Uploadfile(FlaskForm):
	file = FileField(u'Excel File', validators=[DataRequired()])
	submit2 = SubmitField('Upload')

class ChartForm(FlaskForm):
	skill = SelectField('Select skill', choices=[])
	month = SelectField('Select month', choices=[])
	submit = SubmitField('Generate Graph')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SignUpForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField("Username", validators=[DataRequired()])
	employee_id = IntegerField("Employee ID:", validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must match!")])
	pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('Register')

class MakeAdmin(FlaskForm):
    user=SelectField('Select user', choices=[], validators=[DataRequired()])
    submit = SubmitField('Make admin')


class AddProject(FlaskForm):
	project_id = IntegerField("Project ID:", validators=[DataRequired()])
	project_name = StringField("Project Name:")
	project_start_date = DateField("Project Start Date:", format='%Y-%m-%d')
	project_end_date = DateField("Project End Date:", format='%Y-%m-%d')
	submit = SubmitField('Confirm')


class AddEmployee(FlaskForm):
	employee_id = IntegerField("Employee ID:", validators=[DataRequired()])
	employee_first_name = StringField("Employee First Name:", validators=[DataRequired()])
	employee_last_name = StringField("Employee Last Name:")
	employee_hacker_rank_id = StringField("Hacker Rank ID:", validators=[DataRequired()])
	submit1 = SubmitField('Confirm')

class AddSkill(FlaskForm):
	skill_name = StringField("Skill Name:")
	submit = SubmitField('Confirm')

class AssignProject(FlaskForm):
	employee = SelectField('Employee Name', choices=[], validators=[DataRequired()])
	project = SelectField('Project Name', choices=[],  validators=[DataRequired()])
	submit = SubmitField('Confirm')


class SearchEmployee(FlaskForm):
	emp_id = SelectField('Employee Name:', choices=[], validators=[DataRequired()])
	submit = SubmitField('Confirm')

class SearchProject(FlaskForm):
	pro_id = SelectField('Project Name:', choices=[], validators=[DataRequired()])
	submit = SubmitField('Confirm')

class AddScore(FlaskForm):
	employee = SelectField('Employee Name:', choices=[], validators=[DataRequired()])
	skill = SelectField('Skill Name:', choices=[],  validators=[DataRequired()])
	month = SelectField("Month:", choices=[('Jan', 'Jan'),('Feb', 'Feb'),('Mar', 'Mar'),('Apr', 'Apr'),('May', 'May'),('Jun', 'Jun'),('Jul', 'Jul'),('Aug', 'Aug'),('Sep', 'Sep'),('Oct', 'Oct'),('Nov', 'Nov'),('Dec', 'Dec')], validators=[DataRequired()] )
	score =  IntegerField('Score:', validators=[DataRequired()])
	submit = SubmitField('Confirm:')