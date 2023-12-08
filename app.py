from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
from reservation_utils import check_seat_availability, generate_reservation_code, calculate_cost, generate_seating_chart, save_reservation
from authentication_utils import validate_admin_credentials
from admin_utils import calculate_total_sales

# Initialize a Flask application
app = Flask(__name__)
app.config["DEBUG"] = True

# Set a secret key to secure the session data
app.config['SECRET_KEY'] = 'your secret key'

# Define a route for the home page
@app.route('/')
def home():
    # Render the home page template
    return render_template('home.html')

# Define a route to handle the menu option selection
@app.route('/handle-menu-option', methods=['POST'])
def handle_menu_option():
    menu_option = request.form.get('menu_option')

    if menu_option == 'reserve':
        # Generate the current seating chart
        chart = generate_seating_chart()
        # Pair each row with its number and render the reservation page
        labeled_chart = list(enumerate(chart, start=1))
        return render_template('reserve.html', seating_chart=labeled_chart)
    elif menu_option == 'login':
        # Redirect to the admin login page if 'login' is selected
        return redirect(url_for('render_admin_login'))

    # Return a 400 Bad Request if the menu_option is invalid
    abort(400)

# Define a route for the admin login form
@app.route('/admin-login', methods=['GET'])
def render_admin_login():
    # Render the admin login form template
    return render_template('admin-login.html')

# Define a route to handle admin login submissions
@app.route('/admin-login', methods=['POST'])
def handle_admin_login():
    # Extract username and password from the form
    username = request.form['username']
    password = request.form['password']

    # Validate admin credentials
    if validate_admin_credentials(username, password):
        # Set session flag for admin login and redirect to admin dashboard
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        # Flash an error message and redirect to the login form
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('render_admin_login'))

# Define a route for the reserve page
@app.route('/reserve')
def reserve():
    # Generate the current seating chart
    chart = generate_seating_chart()
    # Pair each row with its number and render the reservation page
    labeled_chart = list(enumerate(chart, start=1))
    return render_template('reserve.html', seating_chart=labeled_chart)

# Define a route for the admin dashboard
@app.route('/admin-dashboard')
def admin_dashboard():
    # Check if the user is logged in as admin
    if not session.get('admin_logged_in'):
        # Flash an error message and redirect to the login form
        flash('Please log in as admin first.', 'error')
        return redirect(url_for('render_admin_login'))
    
    # Generate the current seating chart and calculate total sales
    chart = generate_seating_chart()
    labeled_chart = list(enumerate(chart, start=1))
    total_sales = calculate_total_sales()
    # Render the admin dashboard template with the seating chart and total sales
    return render_template('admin-dashboard.html', seating_chart=labeled_chart, total_sales=total_sales)

# Define a route to handle seat reservation requests
@app.route('/reserve_seat', methods=['POST'])
def reserve_seat():
    try:
        # Extract form data for reservation
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        
        # Validate that the names contain only letters
        if not (first_name.isalpha() and last_name.isalpha()):
            message = "First and Last Name should contain only letters. Please go back and try again."
            # If validation fails, regenerate the seating chart and display the reservation page with an error message
            chart = generate_seating_chart()
            labeled_chart = list(enumerate(chart, start=1))
            return render_template('reserve.html', seating_chart=labeled_chart, message=message)

        # Parse and validate the seat row and column
        seat_row = int(request.form.get('seatRow'))
        seat_column = int(request.form.get('seatColumn'))
        
        if not all([first_name, last_name, seat_row, seat_column]):
            # Handle missing information in the form submission
            return "Missing information. All fields are required."

        # Check if the selected seat is available
        if check_seat_availability(seat_row, seat_column):
            # Generate a reservation code and calculate the cost
            reservation_code = generate_reservation_code(first_name, last_name, seat_row, seat_column, "data_files/reservations.txt")
            cost = calculate_cost(seat_row, seat_column)
            # Save the reservation and display a success message
            save_reservation(first_name, last_name, seat_row, seat_column, reservation_code)
            message = f"Reservation Successful! Your code is {reservation_code}. Cost: ${cost}"
        else:
            # Handle case where the seat is already booked
            message = "Seat already booked. Please choose a different seat."
        
        # Regenerate the seating chart and display the reservation page with the message
        chart = generate_seating_chart()
        labeled_chart = list(enumerate(chart, start=1))
        return render_template('reserve.html', seating_chart=labeled_chart, message=message)
    
    except ValueError:
        # Handle invalid input in the form
        return "Invalid input. Please ensure that all fields are filled correctly."

    except Exception as e:
        # Handle any other exceptions that occur
        return f"An internal error occurred: {e}"

# Run the Flask application
app.run(host="0.0.0.0", port=5002)
