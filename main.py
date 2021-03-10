from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
# TODO: is secret key needed for this project?
app.secret_key = 'your secret key'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# TODO: ask professor about proper passwords for website.
app.config['MYSQL_PASSWORD'] = 'mysql' # change this back to 'root' if changed
# TODO: change database name for uniforimity in project.
app.config['MYSQL_DB'] = 'braindb'

# Intialize MySQL
mysql = MySQL(app)

# TODO: Finish Index page 
# index/home page of website
@app.route('/')
@app.route('/home')
def index():
    # Webpage Title
    title = 'Brainfilms - Home'
    selected_term = ''
    # TODO: pull data from categories and subcategories to populate scrollboxes
    # typically the thumbs would be pulled from AI... not active atm
    # Populated from MySQL
    primary_terms =[
        'Other', 'Agriculture', 'Animals & Wildlife', 'Anthropology', 'Archaeology', 'Architecture', 'Art',
        'Biology', 'Chemistry', 'Computer Science', 'Development'
    ]

    # These results should be filtered based on selected_term
    secondary_terms =[
        'DIY & How-To', 'Economics', 'Education', 'Engineering', 'Environment', 'Film & Media', 'Food & Cooking',
        'Geography', 'Geology & Earth', 'Health', 'History', 'Language', 'Law', 'Literature', 'Marketing'
    ]

    # List of filtered terms that will depend on what the selected term is from primary terms.
    filtered_terms =[
        n for n in secondary_terms
            if selected_term in n
    ]


    return render_template('index.html', title = title, primary_terms = primary_terms, filtered_terms = filtered_terms)

# renamed from / to /login as it is no longer splash page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM UserInfo WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Go to Profile page
            return profile(account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

# TODO: Logout not currently used
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # TODO: Redirect to homepage, not sure if this is correct syntax
   return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'firstname' in request.form and'lastname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        # Create variables for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # TODO: form input of creation date.

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM UserInfo WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not firstname or not lastname or not username or not password or not email:
            msg = 'Please fill out the form!'

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO UserInfo (firstname, lastname, username, password, email) VALUES (%s, %s, %s, %s, %s)', (firstname, lastname, username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# Profile Page - Implemented as part of Lab 2
@app.route('/profile', methods = ['GET', 'POST'])
def profile(account):    
    return render_template('profile.html', username = account['username'],
     password = account['password'], firstname=account['firstname'], lastname=account['lastname'],
     email=account['email'])

# TODO: implement add_new fully as a page
@app.route('/add_new')
def add_new():
    return render_template('add_new.html')

# TODO: implement search_result fully as page
@app.route('/search_results')
def search_results():
    # dummy data for testing before implementing database
    searchterm = 'DemoTestingDataDELETEME'
    results = [
        {'res-url': 'www.dumb.com', 'title': 'Dumb Video Website', 'rating': '4', 'date_posted': 'April 20, 2222', 'description': 'This is a dumb video website blah blah balah'},
        {'res-url': 'www.IDKWHy.com', 'title': 'This is Bad', 'rating': '7', 'date_posted': 'April 1, 2011', 'description': 'Greatest bad information ever!'},
        {'res-url': 'www.Study-Stuff.com', 'title': 'This is the best Worst you wille3ver know', 'rating': '0', 'date_posted': 'June 20, 1984', 'description': 'I will highly rate this 0 because of its quality awfulness'}
    ]
    return render_template('search_results.html', title = searchterm, results = results)



####
# Bottom method of code
if __name__ == '__main__':
    app.run(debug=True) #debug is currently enabled for stack traces
# Do not add mmethods below this one.