from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from forms import AddCategoryForm, AddVideoForm, AdvancedSearchForm, IndexSearchBar
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
    indexsearchbar = IndexSearchBar()

    return render_template('index.html', title = title, indexsearchbar = indexsearchbar, loggedin = validate_login(), is_admin = validate_admin())

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
            session['account'] = account

            # Check if user is admin
            cursor.execute(f'SELECT * FROM Admin WHERE id = {account["id"]}')
            is_admin = cursor.fetchone()
            if is_admin:
                session['is_admin'] = True
            else:
                session['is_admin'] = False

            # Go to Profile page
            return redirect(url_for('profile'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', title = title, msg=msg, loggedin = validate_login(), is_admin = validate_admin())

# TODO: Logout not currently used
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    session.pop('account', None)
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
    return render_template('register.html', title = title, msg=msg, loggedin = validate_login(), is_admin = validate_admin())

# Profile Page - Implemented as part of Lab 2
@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if session.get('account'):
        account = session['account']
        title = 'Profile'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM User_Liked_Videos Inner Join Video on User_Liked_Videos.video_id = video.video_id WHERE username = "{account["username"]}"')
        liked_videos = cursor.fetchall()
        return render_template('profile.html', title = title, username = account['username'],
         password = account['password'], liked_videos=liked_videos,
         email=account['email'], creation_date=account['date'], is_admin = validate_admin(), loggedin = validate_login())
    else:
        return render_template('login.html', title = 'Profile Login', msg='Please login',
                               loggedin = validate_login(), is_admin = validate_admin())

@app.route('/admin_dashboard')
def admin():
    return profile()

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
    


@app.route('/admin_add', methods = ['GET', 'POST'])
def add_admin():
    if validate_admin():
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
        return render_template('add_admin.html', msg=msg, loggedin = validate_login(), is_admin = validate_admin())
    else:
        return render_template('admin.html', username=None, is_admin=False, loggedin = validate_login())

@app.route('/admin_video_approval', methods=['GET', 'POST'])
def video_approval():
    if validate_admin():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'approve_video' in request.form:
            cursor.execute(f'DELETE FROM PENDING_VIDEOS WHERE VIDEO_ID = {request.form["approve_video"]}')
            mysql.connection.commit()
        if request.method == 'POST' and 'remove_video' in request.form:
            removal = request.form['remove_video']
            cursor.execute(f'DELETE FROM PENDING_VIDEOS WHERE VIDEO_ID = {removal}')
            cursor.execute(f'DELETE FROM Video_Category WHERE VIDEO_ID = {removal}')
            cursor.execute(f'DELETE FROM User_Liked_Videos WHERE VIDEO_ID = {removal}')
            cursor.execute(f'DELETE FROM User_Rated_videos WHERE VIDEO_ID = {removal}')
            cursor.execute(f'DELETE FROM VIDEO WHERE VIDEO_ID = {removal}')
            mysql.connection.commit()
        cursor.execute('SELECT * FROM Pending_Videos Inner Join Video On Pending_videos.video_id = video.video_id')
        pending_videos = cursor.fetchall()
        return render_template('pending_videos.html', videos = pending_videos , loggedin = validate_login(), is_admin = validate_admin())
    else:
        return render_template('admin.html', username=None, is_admin=False, loggedin = validate_login())

@app.route('/admin_add_category', methods=['GET', 'POST'])
def add_category():
    if validate_admin():
        # Form created for tepmlating
        add_category_form = AddCategoryForm()
        return render_template('add_category.html', add_category_form=add_category_form, loggedin=validate_login(), is_admin = validate_admin())
    return render_template('admin.html', username=None, is_admin=False, loggedin=validate_login())

@app.route('/admin_remove_category', methods=['GET', 'POST'])
def remove_category():
    if validate_admin():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            if 'primary_removal' in request.form:
                cursor.execute(f'Select * from Categories where parent_category = {request.form["primary_removal"]}')
                secondaries_to_delete = cursor.fetchall()
                for secondary in secondaries_to_delete:
                    category_id = secondary['category_id']
                    cursor.execute(f'Select * from Categories where parent_category = {category_id}')
                    tertiaries_to_delete = cursor.fetchall()
                    for tertiary in tertiaries_to_delete:
                        tertiary_id = tertiary['category_id']
                        cursor.execute(f'Delete from video_category where category_id = {tertiary_id}')
                        cursor.execute(f'Delete from categories where category_id = {tertiary_id}')
                        mysql.connection.commit()
                    cursor.execute(f'Delete from video_category where category_id = {category_id}')
                    cursor.execute(f'Delete from categories where category_id = {category_id}')
                    mysql.connection.commit()
                cursor.execute(f'Delete from video_category where category_id = {request.form["primary_removal"]}')
                cursor.execute(f'Delete from categories where category_id = {request.form["primary_removal"]}')
                mysql.connection.commit()
            if 'secondary_removal' in request.form:
                cursor.execute(f'Select * from Categories where parent_category = {request.form["secondary_removal"]}')
                tertiaries_to_delete = cursor.fetchall()
                for tertiary in tertiaries_to_delete:
                    tertiary_id = tertiary['category_id']
                    cursor.execute(f'Delete from video_category where category_id = {tertiary_id}')
                    cursor.execute(f'Delete from categories where category_id = {tertiary_id}')
                    mysql.connection.commit()
                cursor.execute(f'Delete from video_category where category_id = {request.form["secondary_removal"]}')
                cursor.execute(f'Delete from categories where category_id = {request.form["secondary_removal"]}')
                mysql.connection.commit()
            if 'tertiary_removal' in request.form:
                cursor.execute(f'Delete from video_category where category_id = {request.form["tertiary_removal"]}')
                cursor.execute(f'Delete from categories where category_id = {request.form["tertiary_removal"]}')
                mysql.connection.commit()
        cursor.execute('Select * from Categories where parent_category is null')
        primary_categories = cursor.fetchall()
        cursor.execute('select * from (select * from categories) s inner join (select * from categories where parent_category is null) p on s.parent_category = p.category_id')
        secondary_categories = cursor.fetchall()
        cursor.execute('Select distinct s.category_id, s.category_name from Categories s inner join Categories t on s.parent_category = t.category_id where t.parent_category is not null')
        tertiary_categories = cursor.fetchall()
        return render_template('remove_category.html', loggedin=validate_login(), secondary_categories=secondary_categories,
                               is_admin=validate_admin(), primary_categories = primary_categories, tertiary_categories = tertiary_categories)
    return render_template('admin.html', username=None, is_admin=False, loggedin=validate_login())


@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    title = 'Add New Video'
    page = 'add_new.html'
    addvideoform = AddVideoForm()

    if request.method == 'POST' and request.get_json():
        newvideo = request.get_json()

        video_title = newvideo['video_title']
        video_url = newvideo['video_url']
        category_id = newvideo['category_id']
        category_name = newvideo['category_name']
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
                return f"A video with url: {video_url} already exists!"
            else:
                cursor.execute(addvideosql, (video_url, video_title, date_added,))
                cursor.execute(addvideocategorysql, (category_id,))
                mysql.connection.commit()
                cursor.execute(f"Select video_id From Video Where video_url = '{video_url}'")
                video = cursor.fetchone()
                cursor.execute(f"INSERT INTO Pending_Videos (video_id) VALUES ({video['video_id']})")
                mysql.connection.commit()
                return f"New Video: {video_title} added under Category: {category_name}."

    return render_template(page, title = title, addvideoform=addvideoform, loggedin = validate_login(), is_admin = validate_admin())

# Helper for search_results() to query db with id of a category and a regexp searchterm
def dbsearch(selectid, searchterm):
    category_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    category_sql = 'SELECT DISTINCT video.* FROM video JOIN video_category using(video_id) WHERE category_id IN %s'

    term_category_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    tcsql = 'SELECT DISTINCT video.* FROM video JOIN video_category using(video_id) WHERE category_id IN %s HAVING video.video_title REGEXP_LIKE %s'

    if searchterm != "":
        term_category_cursor.execute(tcsql, [(selectid,), searchterm])
        results = term_category_cursor.fetchall()
    else:
        category_cursor.execute(category_sql, [(selectid, )])
        results = category_cursor.fetchall()
    
    return results

@app.route('/search_results', methods = ['GET'])
def search_results():
    args = request.args
    title = "Search Results"
    page = 'search_results.html'

    if args:
        searchterm = '|'.join(args.get('searchterm').split())

        if args.get("tertiaryfilterbool") == 'y':
            results = dbsearch(args.get('tertiaryselect'), searchterm)

        elif args.get("secondaryfilterbool") == 'y':
            results = dbsearch(args.get('secondaryselect'), searchterm)

        elif args.get("primaryselect"):
            results = dbsearch(args.get('primaryselect'), searchterm)
        
        else:
            if searchterm != '':
                term_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                term_sql = 'SELECT * FROM Video WHERE video_title REGEXP %s'
                term_cursor.execute(term_sql, (searchterm,))
                results = term_cursor.fetchall()
            else:
                nullsearch = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                selectallsql = 'SELECT * FROM Video'
                nullsearch.execute(selectallsql,)
                results = nullsearch.fetchall()

        
        return render_template(page, title = title, results=results, loggedin = validate_login(), is_admin = validate_admin())

    return render_template(page, title = title, loggedin = validate_login(), is_admin = validate_admin())

@app.route('/advanced_search', methods = ['GET','POST'])
def advanced_search():
    title = 'Advanced Search'
    advancedsearchform = AdvancedSearchForm()

    return render_template('advanced_search.html', title = title, advancedsearchform = advancedsearchform, loggedin = validate_login(), is_admin = validate_admin())

@app.route('/video-<video_id>', methods = ['GET', 'POST'])
def comments(video_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT * FROM Video WHERE video_id = {video_id}')
    video_found = cursor.fetchone()
    results = None
    if not video_found:
        msg = 'Video not found'
        return render_template('comments.html', msg = msg, loggedin = validate_login(), is_admin = validate_admin())
    else:
        if request.method == 'POST':
            if 'comment' in request.form:
                formatted_date = datetime.now().strftime(datestring)
                cursor.execute(f'INSERT INTO Video_Comments (video_id, username, timestamp, comment) VALUES ({video_id}, "{session["username"]}", "{formatted_date}", "{request.form["comment"]}")')
            if 'timestamp' in request.form:
                cursor.execute(f'Delete from Video_Comments WHERE video_id = {video_id} AND username = "{request.form["username"]}" AND timestamp = "{request.form["timestamp"]}"')
            if 'liked' in request.form:
                cursor.execute(f'INSERT Into User_Liked_Videos (video_id, username) VALUES ({video_id}, "{session["username"]}")')
            if 'unliked' in request.form:
                cursor.execute(f'DELETE FROM User_Liked_Videos where video_id = {video_id}')
            if 'rating' in request.form:
                cursor.execute(f'INSERT INTO User_Rated_Videos (video_id, username, rating) VALUES ({video_id}, "{session["username"]}", {int(request.form["rating"])})')
            mysql.connection.commit()
        cursor.execute(f'SELECT * FROM Video_comments WHERE video_id = {video_id}')
        results = cursor.fetchall()
        user = None
        rating = None
        liked = False
        if session.get('username') and session['username']:
            user = session['username']
            cursor.execute((f'SELECT * FROM User_liked_videos where (video_id, username) = (%s, %s)'), ({video_id}, {session["username"]}))
            result = cursor.fetchone()
            if result:
                liked = True
            cursor.execute((f'SELECT * FROM User_Rated_videos where (video_id, username) = (%s, %s)'), ({video_id}, {session['username']}))
            result = cursor.fetchone()
            if result:
                rating = result['rating']
        return render_template('comments.html', results = results, video_id = video_id, msg = None,
                               loggedin = validate_login(), user = user, video_title = video_found['video_title'],
                               date_added = video_found['date_added'], is_admin = validate_admin(),
                               rating=rating, liked=liked
                               )

def validate_login():
    if session.get('loggedin') and session['loggedin']:
        return True
    return False

def validate_admin():
    if session.get('is_admin') and session['is_admin']:
        return True
    return False

####
# Bottom method of code
if __name__ == '__main__':
    app.run(debug=True) #debug is currently enabled for stack traces
# Do not add mmethods below this one.