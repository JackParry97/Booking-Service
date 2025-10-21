from sqlalchemy.orm import backref
from application import db
from datetime import date

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    postcode = db.Column(db.String(8), unique=True, nullable=False)
    booking = db.relationship('Booking', backref='customer', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    access_level = db.Column(db.String(20), nullable=False)
    bookings = db.relationship('EmpAssigned', backref='employee', lazy=True)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    bookings = db.relationship('BookingJobs', backref='jobs', lazy=True)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('JobMaterials', backref='material', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date_booked = db.Column(db.Date, nullable=False, default=date.today)
    preferred_date = db.Column(db.Date, nullable=False) # Preferred date selected by customer
    date_scheduled = db.Column(db.Date(20), nullable=True) # Scheduled date for the job set by employee
    time_scheduled = db.Column(db.String(20), nullable=True) # Scheduled time for the job set by employee
    status = db.Column(db.String(20), nullable=False, default='Pending') # e.g., Pending, In Progress, Completed --- when status is changed to completed, moved to CompletedJobs table
    emp_assigned = db.relationship('EmpAssigned', backref='booking', lazy=True)
    booking_jobs = db.relationship('BookingJobs', backref='booking', lazy=True)

class EmpAssigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)


class BookingJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    job_materials = db.relationship('JobMaterials', backref='booking_jobs', lazy=True)

class JobMaterials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_jobs_id = db.Column(db.Integer, db.ForeignKey('booking_jobs.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class AdminCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

class CompletedJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    date_completed = db.Column(db.Date, nullable=False, default=date.today)
    total_cost = db.Column(db.Float, nullable=False)
    status_of_payment = db.Column(db.String(20), nullable=False, default='Unpaid')  # e.g., Unpaid, Paid