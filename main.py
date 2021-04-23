from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from forms import AddCategoryForm, AddVideoForm
import MySQLdb.cursors
import re
import json


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
# Secret key is important for WTForms
# TODO: Change to random characters for production
app.config['SECRET_KEY'] = 'BrainLabsTemporary'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# TODO: ask professor about proper passwords for website.
app.config['MYSQL_PASSWORD'] = 'mysql' # change this back to 'root' if changed
# TODO: change database name for uniforimity in project.
app.config['MYSQL_DB'] = 'braindb'
# Datestring used mutliple times for formatting
datestring = '%Y-%m-%d %H:%M:%S'

# Intialize MySQL
mysql = MySQL(app)

# TODO: Finish Index page 
# index/home page of website
@app.route('/')
@app.route('/home')
def index():
    # Webpage Title
    title = 'Brainfilms - Home'
    return render_template('index.html', title = title)

# renamed from / to /login as it is no longer splash page
@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
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

            # Check if user is admin
            cursor.execute(f'SELECT * FROM Admin WHERE id = {account["id"]}')
            is_admin = cursor.fetchone()
            if is_admin:
                session['is_admin'] = True
                return admin()
            else:
                session['is_admin'] = False

            # Go to Profile page
            return profile(account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', title = title, msg=msg)

# TODO: Logout not currently used
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    # TODO: Redirect to homepage, not sure if this is correct syntax
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Formatted date for mysql entry
        formatted_date = datetime.now().strftime(datestring)

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

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO UserInfo (username, password, email, date) VALUES (%s, %s, %s, %s)', (username, password, email,formatted_date,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', title = title, msg=msg)

# Profile Page - Implemented as part of Lab 2
@app.route('/profile', methods = ['GET', 'POST'])
def profile(account):
    title = 'Profile'    
    return render_template('profile.html', title = title, username = account['username'],
     password = account['password'],
     email=account['email'], creation_date=account['date'])


@app.route('/populateprimaryselect', methods = ['POST'])
def populateprimaryselect():
    tuple_cursor = mysql.connection.cursor(MySQLdb.cursors.SSCursor)
    tc_sql = "select category_id, category_name from categories where parent_category is null order by category_name asc"
    tuple_cursor.execute(tc_sql,)
    category_tuples = tuple_cursor.fetchall()
    if category_tuples:
        primaryjson = [{'category_id': category_id, 'category_name': category_name} for category_id, category_name in category_tuples]
        return jsonify(primaryjson)
    return {}



@app.route('/populatefilteredselect', methods = ['POST'])
def populatefilteredselect():
    if request.method == 'POST' and request.form['category_id'] != 0:
        tuple_cursor = mysql.connection.cursor(MySQLdb.cursors.SSCursor)
        tc_sql = "select category_id, category_name from categories where parent_category = %s order by category_name asc"
        tuple_cursor.execute(tc_sql, (request.form['category_id'],))
        category_tuples = tuple_cursor.fetchall()
        if category_tuples:
            secondaryjson = [{'category_id': category_id, 'category_name': category_name} for category_id, category_name in category_tuples]
            return jsonify(secondaryjson)
    return {}


@app.route('/addcategorytodb', methods=["POST"])
def addcategorytodb():
    newcategory = request.get_json()
    # Spellchecking for uniform data
    category_name = newcategory['category_name'].capitalize()
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    checksql = "select * from categories where category_name = %s"
    insert_primary_sql = 'INSERT INTO Categories (category_name, parent_category) VALUES (%s, null)'
    insert_subclass_sql = 'INSERT INTO Categories (category_name, parent_category) VALUES (%s, %s)'
    cursor.execute(checksql, (category_name,))
    # Duplicate check
    dupe_exists = cursor.fetchone()
    if dupe_exists:
        return category_name + " already exists! Use a different Category Name."
    # If duplicate passes
    else:
        # Create new Primary category
        if request.method == 'POST' and newcategory['primarybool']:
            cursor.execute(insert_primary_sql, (category_name,))
            mysql.connection.commit()
            msg = f"{category_name} created as a Primary Category!"
            return msg
        
        # Create new Secondary category
        if request.method == 'POST' and newcategory['secondarybool']:
            primary_id = newcategory['primary_id']
            cursor.execute(insert_subclass_sql, (category_name, primary_id,))
            mysql.connection.commit()
            msg = f"{category_name} created as a Secondary Category!"
            return msg

        # Create new Tertiary category
        if request.method == 'POST' and newcategory['primary_id'] and newcategory['secondary_id']:
            secondary_id = newcategory['secondary_id']
            cursor.execute(insert_subclass_sql, (category_name, secondary_id,))
            mysql.connection.commit()
            msg = f"{category_name} created as a Tertiary Category!"
            return msg
    return 'Something went wrong!'
    


@app.route('/admin/dashboard', methods = ['GET', 'POST'])
def admin():
    # Form created for tepmlating
    add_category_form = AddCategoryForm()
    
    admin_page_var = 'admin.html'
    if session.get('is_admin') and session['is_admin']:
        return render_template(admin_page_var, username = session['username'], is_admin=True, add_category_form=add_category_form)
    else:
        return render_template(admin_page_var, username=None, is_admin=False)

@app.route('/admin/dashboard/add', methods = ['GET', 'POST'])
def add_admin():
    if session.get('is_admin') and session['is_admin']:
        msg = ''
        if request.method == 'POST' and 'username' in request.form:
            username = request.form['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f'SELECT * FROM UserInfo WHERE username = "{username}"')
            account = cursor.fetchone()
            if account:
                # Check if user is already admin
                cursor.execute(f'SELECT * FROM Admin WHERE id = {account["id"]}')
                is_admin = cursor.fetchone()
                if is_admin:
                    msg = 'User is already admin'
                else:
                    cursor.execute(f'INSERT INTO ADMIN(id) VALUES({account["id"]})')
                    mysql.connection.commit()
                    msg = 'User successfully added'
            else:
                msg = 'User not found'
        return render_template('add_admin.html', msg=msg)
    else:
        return render_template('admin.html', username=None, is_admin=False)

@app.route('/addvideotodb', methods=['POST'])
def addvideotodb():
    newvideo = request.get_json()

    video_title = newvideo['video_title']
    video_url = newvideo['video_url']
    category_id = newvideo['category_id']
    date_added = datetime.now().strftime(datestring)
    addvideosql = "INSERT INTO Video (video_url, video_title, date_added) VALUES (%s, %s, %s)"
    addvideocategorysql = "INSERT INTO Video_Category (video_id, category_id) VALUES (LAST_INSERT_ID(), %s)"

    if video_url:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Duplicate Check
        checksql = "select * from video where video_url = %s"
        cursor.execute(checksql, (video_url,))
        dupe_exists = cursor.fetchone()
        if dupe_exists:
            return "A video already exists with that URL!"
        else:
            cursor.execute(addvideosql, (video_url, video_title, date_added,))
            cursor.execute(addvideocategorysql, (category_id,))
            mysql.connection.commit()
            return "added! (but not really)"
    return {}



@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    title = 'Add New Video'
    page = 'add_new.html'
    addvideoform = AddVideoForm()
    return render_template(page, title = title, addvideoform=addvideoform)


@app.route('/search_results', methods = ['GET', 'POST'])
def search_results():
    args = request.args
    title = "Search Results"
    page = 'search_results.html'
    # TODO: remove test prints
    key_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    key_sql = 'SELECT * FROM Video WHERE video_title REGEXP %s'

    filter_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    filter_sql = 'SELECT DISTINCT video.* FROM video JOIN video_category using(video_id) WHERE sub_id IN %s'

    multi_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    multi_sql = 'SELECT DISTINCT video.* FROM video JOIN video_category using(video_id) WHERE sub_id IN %s HAVING video.video_title REGEXP %s'

    if args:
        if (args.get("search-term") != "") and args.get("filterID"):
            multi_cursor.execute(multi_sql, [args.getlist("filterID")," ".join(args.get("search-term").split()).replace(" ", "|")])
            results = multi_cursor.fetchall()
            return render_template(page, title = title, results = results)

        elif args.get("search-term") != "":
            # Search OR keyword
            key_cursor.execute(key_sql, (" ".join(args.get("search-term").split()).replace(" ", "|"),))
            # Search And Keyword
            # key_cursor.execute(key_sql, (" ".join(args.get("search-term").split()).replace(" ", "&"),))
            results = key_cursor.fetchall()
            return render_template(page, title = title, results=results)

        elif args.get("filterID"):
            filter_cursor.execute(filter_sql, [args.getlist("filterID")])
            results = filter_cursor.fetchall()
            return render_template(page, title = title, results=results)
        
        # TODO: determine if this can be avoided with regexp searching or parsing query string
        elif args.get("search-term") == "":
            key_cursor.execute('SELECT * FROM video',)
            results = key_cursor.fetchall()
            return render_template(page, title = "All Videos", results=results)

    return render_template(page, title = title)

@app.route('/advanced_search', methods = ['GET','POST'])
def advanced_search():
    title = 'Advanced Search'
    # Populate dropdown menus from mysql
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Select everything alphabetically
    cursor.execute('SELECT * FROM Category ORDER BY name')
    categories = cursor.fetchall()
    # TODO: These results should be filtered based category
    cursor.execute('SELECT * FROM Subcategory ORDER BY sub_name')
    subcategories = cursor.fetchall()

    return render_template('advanced_search.html', title = title, categories = categories, subcategories = subcategories)


####
# Bottom method of code
if __name__ == '__main__':
    app.run(debug=True) #debug is currently enabled for stack traces
# Do not add mmethods below this one.