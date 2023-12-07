import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

#flash the secret key to secure sessions
app.config['SECRET KEY'] = 'your secret key'

#append info to data_files / ..txt
def data_files_write(filename, content):
    try:
        passcodesFile = open("data_files/passcodes.txt", "a")  
        reservationsFile = open("data_files/reservations.txt", "a")  
    except:
        print("file does not exsist")
    if filename == "passcodes":
        passcodesFile.write(f"{content}\n")
    elif filename == "reservations":
        reservationsFile.write(f"{content}\n")
    else:
        print("filename should be passcodes or reservations")
    passcodesFile.close()
    reservationsFile.close()


#function to get a list of passcodes
def get_passcodes():
    passcodes = []
    try:
        passcodesFile = open("data_files/passcodes.txt")
        for line in passcodesFile:
            passcodes.append(line.removesuffix('\n'))
    except:
        print("file does not exsist") 
    passcodesFile.close()

    return passcodes


#function to get a list of passcodes
def get_reservations():
    reservations = []
    try:
        reservationsFile = open("data_files/reservations.txt")  
        for line in reservationsFile:
            reservations.append(line.removesuffix('\n'))
    except:
        print("file does not exsist") 
    reservationsFile.close()

    return reservations


# use the app.route() decorator to create a Flask view function called index()
@app.route('/', methods=('GET', 'POST'))
def home():
    menu_option = ['login', 'reserve']

    if request.method == "POST":
        option = request.form['option']

        if not option:
            flash("must select menu option")

    # if option == 'login':
    #     #redirect to login 
            #return redirect("login.html", code=302)
    # if option == 'reserve':
    #     #redirect to reserve
            #return redirect("reserve.html", code=302)


    return render_template('home.html', menu_option=menu_option)

@app.route('/handle-menu-option', methods=['POST'])
def handle_menu_option():
    menu_option = request.form.get('menu_option')

    if menu_option == 'reserve':
        # Add reservation logic here (e.g., call a function to handle the reservation)

        # Render the reserve.html template
        return render_template('reserve.html')

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

# Function to read admin credentials from passcodes.txt
def read_admin_credentials():
    admin_credentials = []
    #match admin credentials to the passcodes.txt file
    try:
        with open("data_files/passcodes.txt", "r") as passcodes_file:
            for line in passcodes_file:
                username, password = map(str.strip, line.split(','))
                admin_credentials.append((username, password))
    except FileNotFoundError:
        print("passcodes.txt not found")

    return admin_credentials

# Route for the admin dashboard
@app.route('/admin-dashboard')
def admin_dashboard():
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        # Redirect to the admin login page if not logged in
        flash('Please log in as admin first.', 'error')
        return redirect(url_for('admin_login'))


    return render_template('admin-dashboard.html')

#Below is just a template and might need to be modified to work.
# @app.route('/create/', methods=('GET', 'POST'))
# def create():

#     if request.method == "POST":
#         #get title and content submitted by user
#         title = request.form['title']
#         content = request.form['content']    

#         #display error if not submitted
#         #otherwise make a database connection and insert the post
#         if not title:
#             flash('Title is required')
#         elif not content:
#             flash('Content is required')
#         else:
#             conn = get_db_connection()
#             insert_query = 'INSERT INTO posts (title, content) VALUES (?, ?)'
#             conn.execute(insert_query, (title, content))
#             conn.commit()
#             conn.close()
#             #redirect to index page when successfully submitted
#             return redirect(url_for('index'))

#     return render_template('create.html')

# #route to edit post
# @app.route('/<int:id>/edit/', methods=('GET', 'POST'))
# def edit(id):
#     #get id from get_post()
#     post = get_post(id)

#     if request.method == "POST":
#         #get title and content submitted by user
#         title = request.form['title']
#         content = request.form['content']    

#         #display error if not submitted
#         #otherwise make a database connection and insert the post
#         if not title:
#             flash('Title is required')
#         elif not content:
#             flash('Content is required')
#         else:
#             conn = get_db_connection()
#             update_query = 'UPDATE posts SET title = ?, content = ? WHERE id = ?'
#             conn.execute(update_query, (title, content, id))
#             conn.commit()
#             conn.close()
#             #redirect to index page when successfully submitted
#             return redirect(url_for('index'))

#     return render_template('edit.html', post=post)


# # route to delete a post
# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     #get the post
#     post = get_post(id)

#     #connect to databse
#     conn = get_db_connection()

#     #run a delete query
#     delete_query = 'DELETE FROM posts WHERE id = ?'
#     conn.execute(delete_query, (id,))

#     #commit changes and close connection to databse
#     conn.commit()
#     conn.close()

#     #show sucess message if deleted
#     flash('{} has been deleted'.format(post['title']))
    
#     #redirect to index page
#     return  redirect(url_for('index'))


app.run(host="0.0.0.0", port=5002)