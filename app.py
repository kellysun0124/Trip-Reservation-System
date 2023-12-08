from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
from reservation_utils import check_seat_availability, generate_reservation_code, calculate_cost, generate_seating_chart, save_reservation
from authentication_utils import read_admin_credentials, get_passcodes
import os

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/handle-menu-option', methods=['POST'])
def handle_menu_option():
    menu_option = request.form.get('menu_option')

    if menu_option == 'reserve':
        chart = generate_seating_chart()
        # Pair each row with its number
        labeled_chart = list(enumerate(chart, start=1))
        return render_template('reserve.html', seating_chart=labeled_chart)
    elif menu_option == 'login':
        # Redirect to the admin login page
        return redirect(url_for('render_admin_login'))

    abort(400)  # Bad request if the menu_option is neither 'reserve' nor 'login'

# Route to render the admin login form
@app.route('/admin-login', methods=['GET'])
def render_admin_login():
    return render_template('admin-login.html')

# Route to handle admin login form submission
@app.route('/admin-login', methods=['POST'])
def handle_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Read admin credentials from the passcodes.txt file
    admin_credentials = read_admin_credentials()

    # Check if the provided credentials match any admin account
    if (username, password) in admin_credentials:
        session['admin_logged_in'] = True
        flash('Admin login successful', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'error')

    # Manually pop flashed messages from the session
    session.pop('_flashes', None)

    return redirect(url_for('render_admin_login'))

@app.route('/reserve')
def reserve():
    chart = generate_seating_chart()
    # Pair each row with its number
    labeled_chart = list(enumerate(chart, start=1))
    return render_template('reserve.html', seating_chart=labeled_chart)

# Route for the admin dashboard
@app.route('/admin-dashboard')
def admin_dashboard():
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        # Redirect to the admin login page if not logged in
        flash('Please log in as admin first.', 'error')
        return redirect(url_for('admin_login'))


    return render_template('admin-dashboard.html')

@app.route('/reserve_seat', methods=['POST'])
def reserve_seat():
    try:
        # Extract form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        seat_row = int(request.form.get('seatRow'))
        seat_column = int(request.form.get('seatColumn'))
        
        # Validate form data
        if not all([first_name, last_name, seat_row, seat_column]):
            return "Missing information. All fields are required."

        # Check seat availability and make the reservation
        if check_seat_availability(seat_row, seat_column):
            reservation_code = generate_reservation_code(first_name, last_name, seat_row, seat_column)
            cost = calculate_cost(seat_row, seat_column)
            save_reservation(first_name, last_name, seat_row, seat_column, reservation_code)
            message = f"Reservation Successful! Your code is {reservation_code}. Cost: ${cost}"
        else:
            message = "Seat already booked. Please choose a different seat."

    except Exception as e:
        message = f"An internal error occurred: {e}"

    return f'{message} <br><br><a href="/reserve">Back to Reservation Page</a>'



app.run(host="0.0.0.0", port=5002)