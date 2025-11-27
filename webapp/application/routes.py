from flask import render_template, request, redirect, url_for
from application import app,db
from application.models import Customer, Employee, Jobs, Material, Booking, EmpAssigned, BookingJobs, JobMaterials
from application.forms import CreateCustomerForm, CreateEmployeeForm, CreateJobForm, CreateMaterialForm, CreateBookingForm, ScheduleJobForm, UpdateStatusForm, EditBookingForm, AddMaterialsForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plumbing')
def plumbing():
    return render_template('plumbing.html')

@app.route('/heating')
def heating():
    return render_template('heating.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/book')
# def book():
#     return render_template('book.html')

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    form = CreateCustomerForm()
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        postcode = form.postcode.data

        if form.validate_on_submit():
            new_customer = Customer(name=name, email=email, phone=phone, address=address, postcode=postcode)
            db.session.add(new_customer)
            db.session.commit()
            # redirect to the create_booking page for this new customer
            return redirect(url_for('create_booking', cust_id=new_customer.id))
    return render_template('create_customer.html', form=form)

@app.route('/create_employee', methods=['GET', 'POST'])
def create_employee():
    form = CreateEmployeeForm()
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        access_level = form.access_level.data

        if form.validate_on_submit():
            new_employee = Employee(name=name, email=email, phone=phone, access_level=access_level)
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create_employee.html', form=form)

@app.route('/create_job', methods=['GET', 'POST'])
def create_job():   
    form = CreateJobForm()
    if request.method == 'POST':
        description = form.description.data
        category = form.category.data
        price_per_hour = form.price_per_hour.data

        if form.validate_on_submit():
            new_job = Jobs(description=description, category=category, price_per_hour=price_per_hour)
            db.session.add(new_job)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create_job.html', form=form)

@app.route('/create_material', methods=['GET', 'POST'])
def create_material():   
    form = CreateMaterialForm()
    if request.method == 'POST':
        manufacturer = form.manufacturer.data
        name = form.name.data
        price = form.price.data

        if form.validate_on_submit():
            new_material = Material(manufacturer=manufacturer, name=name, price=price)
            db.session.add(new_material)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create_material.html', form=form)

@app.route('/create_booking/<int:cust_id>', methods=['GET', 'POST'])
def create_booking(cust_id):
    form = CreateBookingForm()
    # populate choices as (id, label) pairs; SelectMultipleField expects (value, label)
    form.job_id.choices = [(job.id, f"{job.description} ({job.category}) - £{job.price_per_hour}") for job in Jobs.query.all()]

    if request.method == 'POST':
        customer_id = cust_id
        selected_job_ids = form.job_id.data  # this will be a list of ints when using SelectMultipleField
        preferred_date = form.preferred_date.data

        if form.validate_on_submit():
            new_booking = Booking(customer_id=customer_id, preferred_date=preferred_date)
            db.session.add(new_booking)
            db.session.commit()

            # create a BookingJobs record for each selected job
            for jid in selected_job_ids:
                booking_job = BookingJobs(booking_id=new_booking.id, job_id=jid)
                db.session.add(booking_job)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('book.html', form=form)

@app.route('/add_materials', methods=['GET', 'POST'])
def add_materials():
    form = AddMaterialsForm()
    # populate choices for booking jobs and materials
    form.booking_job_id.choices = [(bj.id, f"BookingJob #{bj.id} for Booking #{bj.booking_id}") for bj in BookingJobs.query.all()]

    if request.method == 'POST':
        booking_job_id = form.booking_job_id.data
        material_id = form.material_id.data
        quantity = form.quantity.data

        if form.validate_on_submit():
            # add the specified quantity of the material to the booking job
            
            job_material = JobMaterials(booking_jobs_id=booking_job_id, material_id=material_id, quantity=quantity)
            db.session.add(job_material)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('add_materials.html', form=form)

@app.route('/schedule_job', methods=['GET', 'POST'])
def schedule_job():
    form = ScheduleJobForm()
    # populate choices for bookings and employees
    form.booking_id.choices = [(booking.id, f"Booking #{booking.id} for Customer #{booking.customer_id}") for booking in Booking.query.all()]
    form.employee_id.choices = [(emp.id, emp.name) for emp in Employee.query.all()]

    if request.method == 'POST':
        booking_id = form.booking_id.data
        employee_id = form.employee_id.data
        date_scheduled = form.date_scheduled.data
        time_scheduled = form.time_scheduled.data

        if form.validate_on_submit():
            # update the booking with scheduled date and time
            booking = Booking.query.get(booking_id)
            booking.date_scheduled = date_scheduled
            booking.time_scheduled = time_scheduled
            db.session.commit()

            # create an EmpAssigned record
            emp_assigned = EmpAssigned(booking_id=booking_id, employee_id=employee_id)
            db.session.add(emp_assigned)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('schedule_job.html', form=form)



# # todo later: update status of a booked job from view bookings page and pass booking id to form there instead of selecting from all bookings here
# @app.route('/update_status', methods=['GET', 'POST'])
# def update_status():
#     form = UpdateStatusForm()
#     # populate choices for bookings
#     form.booking_id.choices = [(booking.id, f"Booking #{booking.id} for Customer #{booking.customer_id}") for booking in Booking.query.all()]

#     if request.method == 'POST':
#         booking_id = form.booking_id.data
#         status = form.status.data

#         if form.validate_on_submit():
#             # update the booking status
#             booking = Booking.query.get(booking_id)
#             booking.status = status
#             db.session.commit()

#             return redirect(url_for('index'))
#     return render_template('update_status.html', form=form)

@app.route('/view_bookings')
def view_bookings():   
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)

@app.route('/view_customers')
def view_customers():  
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

@app.route('/view_employees')
def view_employees():   
    employees = Employee.query.all()
    return render_template('view_employees.html', employees=employees)

@app.route('/view_jobs')
def view_jobs():   
    jobs = Jobs.query.all()
    return render_template('view_jobs.html', jobs=jobs)

@app.route('/view_materials')
def view_materials():   
    materials = Material.query.all()
    return render_template('view_materials.html', materials=materials) 

@app.route('/edit_booking/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = EditBookingForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            booking.customer_id = form.customer_id.data
            booking.date_booked = form.date_booked.data
            booking.preferred_date = form.preferred_date.data
            booking.date_scheduled = form.date_scheduled.data
            booking.time_scheduled = form.time_scheduled.data
            booking.status = form.status.data
            # Note: emp_assigned and booking_jobs would typically require more complex handling
            db.session.commit()
            return redirect(url_for('view_bookings'))

    # Pre-populate the form with existing booking data
    elif request.method == 'GET':
        form.booking_id.data = booking.id
        form.customer_id.data = booking.customer_id
        form.date_booked.data = booking.date_booked
        form.preferred_date.data = booking.preferred_date
        form.date_scheduled.data = booking.date_scheduled
        form.time_scheduled.data = booking.time_scheduled
        form.status.data = booking.status
    return render_template('edit_booking.html', form=form)

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CreateCustomerForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            customer.name = form.name.data
            customer.email = form.email.data
            customer.phone = form.phone.data
            customer.address = form.address.data
            customer.postcode = form.postcode.data
            db.session.commit()
            return redirect(url_for('view_customers'))

    # Pre-populate the form with existing customer data
    elif request.method == 'GET':
        form.name.data = customer.name
        form.email.data = customer.email
        form.phone.data = customer.phone
        form.address.data = customer.address
        form.postcode.data = customer.postcode
    return render_template('edit_customer.html', form=form)

@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = CreateEmployeeForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            employee.name = form.name.data
            employee.email = form.email.data
            employee.phone = form.phone.data
            employee.access_level = form.access_level.data
            db.session.commit()
            return redirect(url_for('view_employees'))

    # Pre-populate the form with existing employee data
    elif request.method == 'GET':
        form.name.data = employee.name
        form.email.data = employee.email
        form.phone.data = employee.phone
        form.access_level.data = employee.access_level
    return render_template('edit_employee.html', form=form)

@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    form = CreateJobForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            job.description = form.description.data
            job.category = form.category.data
            job.price_per_hour = form.price_per_hour.data
            db.session.commit()
            return redirect(url_for('view_jobs'))

    # Pre-populate the form with existing job data
    elif request.method == 'GET':
        form.description.data = job.description
        form.category.data = job.category
        form.price_per_hour.data = job.price_per_hour
    return render_template('edit_job.html', form=form)

@app.route('/edit_material/<int:material_id>', methods=['GET', 'POST'])
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    form = CreateMaterialForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            material.manufacturer = form.manufacturer.data
            material.name = form.name.data
            material.price = form.price.data
            db.session.commit()
            return redirect(url_for('view_materials'))

    # Pre-populate the form with existing material data
    elif request.method == 'GET':
        form.manufacturer.data = material.manufacturer
        form.name.data = material.name
        form.price.data = material.price
    return render_template('edit_material.html', form=form)

@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('view_bookings'))

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('view_customers'))

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):   
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('view_employees'))

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):   
    job = Jobs.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('view_jobs'))

@app.route('/delete_material/<int:material_id>', methods=['POST'])
def delete_material(material_id):   
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    return redirect(url_for('view_materials'))

