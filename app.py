import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

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