from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField
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
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

@app.route('/admin/dashboard', methods = ['GET', 'POST'])
def admin():
    #TODO: This is populating the dropdown currently. needs to be done dynamically
    form = CategoryForm()
    c1 = mysql.connection.cursor(MySQLdb.cursors.SSCursor)
    c1sql = "select category_id, category_name from categories where parent_category is null;"
    c1.execute(c1sql,)
    parents = c1.fetchall()
    form.category.choices = [(k,v) for k,v in parents]

    admin_page_var = 'admin.html'
    if session.get('is_admin') and session['is_admin']:
        return render_template(admin_page_var, username = session['username'], is_admin=True, form=form)
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

@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    title = 'Add New'
    # Populate dropdown menus from mysql
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Select everything alphabetically
    cursor.execute('SELECT * FROM Category ORDER BY name')
    categories = cursor.fetchall()
    # TODO: These results should be filtered based category
    cursor.execute('SELECT * FROM Subcategory ORDER BY sub_name')
    subcategories = cursor.fetchall()
    # error message
    msg = ''
    if request.method == 'POST' and 'video_url' in request.form and 'video_title' in request.form:
        # Variables for video
        video_url = request.form['video_url']
        video_title = request.form['video_title']
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if video exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Video WHERE video_url = %s', (video_url,))
        video = cursor.fetchone()

        # If the video url is not unique, show errors:
        if video:
            msg = 'Video with that url already exists!'
            # TODO: possibly return the webpage for that video rating
        elif not video_url or not video_title:
            msg = 'Both url and video title need to be filled in!'
        
        # Add video to database
        else:
            cursor.execute('INSERT INTO Video (video_url, video_title, date_added) VALUES (%s, %s, %s)', (video_url, video_title, date_added,))
            mysql.connection.commit()
            msg = 'Video Added!'

    return render_template('add_new.html', title = title, msg = msg, categories = categories, subcategories = subcategories)


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




# Function checks if a category exists in database already
@app.route("/category_exists", methods=['POST'])
def category_exists():
    msg = ''
    categoryname = request.form['category-name-field']
    try:
        cursorsearch = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT category_name FROM Categories WHERE category_name=%s"
        cursorsearch.execute(sql, categoryname)
        exists = cursorsearch.fetchone()
        if exists:
            msg = 'Category Exists'
        else:
            cursoradd = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursoradd.execute('INSERT INTO Categories (category_name, parent_category) VALUES (%s, %s)', (categoryname, 'null',))
            mysql.connection.commit()
            msg = 'Video Added!'
        return jsonify({'result' : 'success'})

    except Exception as e:
        print(e)

class CategoryForm(FlaskForm):
    category = SelectField('category', choices=[])
    category2 = SelectField('category2', choices=[])
    category3 = SelectField('category3', choices=[])

    





# TODO: Delete this route, for testing only
@app.route("/query")
def query():
    # Test String: /query?query_term=query+strings+with+flask&foo=steven&bar=weeeeeeebar&baz=baz
    # https://www.youtube.com/watch?v=PL6wzmKrgRg
    #check if args exist
    if request.args:
        print(request.query_string)
        # parse query string and serialzise into immutable multi dictionary
        args = request.args
        if "query_term" in args:
            qt = args.get("query_term")
            print(f"QT: {qt}")
        if "bar" in args:
            bar = args["bar"]
            print(bar)
        if "baz" in args:
            print(request.args.get("baz"))
        for k, v in args.items():
            if(k == "title"):
                print(f"TITLE : {k} VALUE : {v}")
            if("foo" in args):
                foo = args.get("foo")
                print(foo)
            print(f"{k} : {v}")
        #serialized strings and string interpolation
        serialized = ", ".join(f"{k}: {v}" for k, v in args.items())
        return f"(Query) {serialized}", 200

    return "query received", 200



####
# Bottom method of code
if __name__ == '__main__':
    app.run(debug=True) #debug is currently enabled for stack traces
# Do not add mmethods below this one.