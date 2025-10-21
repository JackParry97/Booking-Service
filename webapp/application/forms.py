from datetime import date
from flask.app import Flask
from sqlalchemy.orm import query
from wtforms.fields.core import DateField, DecimalField, IntegerField
from application.models import Customers, Materials, Tasks
from flask_wtf.form import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, AnyOf, Email

# Form for creating a new customer. Customer details are required.
class CreateCustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    submit = SubmitField('Create Customer')

# Form for creating a new employee. Employee details are required. Only accessible by employees with admin access.
class CreateEmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    access_level = SelectField('Access Level', choices=[('Admin', 'Admin'), ('Employee', 'Employee')], validators=[DataRequired(), AnyOf(['Admin', 'Employee'])])
    submit = SubmitField('Create Employee')

# Form for creating a new job, e.g., plumbing or heating task. Only accessible by employees with admin access.
class CreateJobForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Plumbing', 'Plumbing'), ('Heating', 'Heating')], validators=[DataRequired(), AnyOf(['Plumbing', 'Heating'])])
    price_per_hour = DecimalField('Price per Hour', validators=[DataRequired()])
    submit = SubmitField('Create Job')

# Form for creating a new material. Only accessible by employees with admin access.
class CreateMaterialForm(FlaskForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    name = StringField('Material Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Create Material')

# Form for selecting a job to book. Customer selects job and preferred date.
class SelectJobForm(FlaskForm):
    job_id = SelectField('Job', coerce=int, validators=[DataRequired()])
    preferred_date = DateField('Preferred Date', validators=[DataRequired()], default=date.today)
    submit = SubmitField('Book Job')

# Form for scheduling a booked job. Employee selects scheduled date and time as well as the employee for the job. ---- Access through 'schedule job' button on edit bookings page.
class ScheduleJobForm(FlaskForm):
    booking_id = SelectField('Booking', coerce=int, validators=[DataRequired()])
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    date_scheduled = DateField('Scheduled Date', validators=[DataRequired()], default=date.today)
    time_scheduled = StringField('Scheduled Time', validators=[DataRequired()])
    submit = SubmitField('Schedule Job')

# Form for updating the status of a booked job. Employee selects new status. ---- Access through 'update status' button on edit bookings page.
class UpdateStatusForm(FlaskForm):  
    booking_id = SelectField('Booking', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], validators=[DataRequired(), AnyOf(['Pending', 'In Progress', 'Completed'])])
    submit = SubmitField('Update Status')

# Form for adding materials to a booked job. Employee selects material and quantity. ---- Access through 'add materials' button on edit bookings page.
class AddMaterialsForm(FlaskForm):  
    booking_job_id = SelectField('Booking Job', coerce=int, validators=[DataRequired()])
    material_id = SelectField('Material', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Materials')

# Form for searching customers by name or email. Employee inputs search term.
class SearchCustomerForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')