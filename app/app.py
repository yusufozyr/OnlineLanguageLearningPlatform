
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'

#MySQL.init_app(app)
mysql = MySQL(app)  



@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/registerL', methods=['GET', 'POST'])
def registerL():
    message = ''
    if request.method == 'POST' and 'full_name' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'nationality' in request.form and 'bdate' in request.form and 'learning_style' in request.form and 'learning_objective' in request.form:
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nationality = request.form['nationality']
        bdate = request.form['bdate']
        learning_style = request.form['learning_style']
        learning_objective = request.form['learning_objective']

        # Check if the username is unique
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE U_id = %s', (username,))
        account = cursor.fetchone()
        if account:
            message = 'Username already exists. Please choose a different username.'
        
        elif not username or not full_name or not email or not password or not nationality or not bdate or not learning_style or not learning_objective:
            message = 'Please fill out the form!'

        else:
            # Insert into User table with U_id equal to username
            cursor.execute(
                'INSERT INTO User (U_id, full_name, email, password, nationality, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)',
                (username, full_name, email, password, nationality, bdate)
            )
            mysql.connection.commit()

            # Insert into Learner table
            cursor.execute(
                'INSERT INTO Learner (U_id, learning_style, learning_objective) VALUES (%s, %s, %s)',
                (username, learning_style, learning_objective)
            )
            mysql.connection.commit()

            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('registerL.html', message=message)

@app.route('/registerT', methods=['GET', 'POST'])
def registerT():
    message = ''
    if request.method == 'POST' and 'full_name' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'nationality' in request.form and 'bdate' in request.form and 'fee_per_hour' in request.form and 'experience' in request.form:
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nationality = request.form['nationality']
        bdate = request.form['bdate']
        fee_per_hour = request.form['fee_per_hour']
        experience = request.form['experince']

        # Check if the username is unique
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE U_id = %s', (username,))
        account = cursor.fetchone()
        if account:
            message = 'Username already exists. Please choose a different username.'
        
        elif not username or not full_name or not email or not password or not nationality or not bdate or not fee_per_hour or not experience:
            message = 'Please fill out the form!'

        else:
            # Insert into User table with U_id equal to username
            cursor.execute(
                'INSERT INTO User (U_id, full_name, email, password, nationality, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)',
                (username, full_name, email, password, nationality, bdate)
            )
            mysql.connection.commit()

            # Insert into Learner table
            cursor.execute(
                'INSERT INTO Teacher (U_id, fee_per_hour, experince) VALUES (%s, %s, %s)',
                (username, learning_style, learning_objective)
            )
            mysql.connection.commit()

            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('registerT.html', message=message)

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE U_id = %s AND password = %s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['U_id']
            session['username'] = user['U_id']

            cursor.execute('SELECT * FROM Learner WHERE U_id = %s', (username,))
            learner = cursor.fetchone()
            if learner:
                message = 'Learner Logged in successfully!'
                return redirect(url_for('menuL'))

            cursor.execute('SELECT * FROM Teacher WHERE U_id = %s', (username,))
            teacher = cursor.fetchone()
            if teacher:
                message = 'Teacher Logged in successfully!'
                return redirect(url_for('menuT'))

        else:
            message = 'Please enter correct User Name and Password!'
        
    return render_template('login.html', message = message)

def get_learner_info(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT User.full_name, User.email, GROUP_CONCAT(Language.Language_name) as languages, GROUP_CONCAT(Language.Language_level) as levels
        FROM User
        LEFT JOIN Current_Level ON User.U_id = Current_Level.U_id
        LEFT JOIN Language ON Current_Level.Language_id = Language.Language_id
        WHERE User.U_id = %s
        GROUP BY User.full_name, User.email
    ''', (user_id,))
    learner_info = cursor.fetchone()
    return learner_info

def get_goal_info(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT User.full_name, User.email, GROUP_CONCAT(Language.Language_name) as languages, GROUP_CONCAT(Language.Language_level) as levels
        FROM User
        LEFT JOIN Goal_Level ON User.U_id = Goal_Level.U_id
        LEFT JOIN Language ON Goal_Level.Language_id = Language.Language_id
        WHERE User.U_id = %s
        GROUP BY User.full_name, User.email
    ''', (user_id,))
    goal_info = cursor.fetchone()
    return goal_info

@app.route('/menuL', methods =['GET', 'POST'])
def menuL():
    if 'loggedin' in session and session['loggedin']:
        # Assuming you store user_id in the session during login
        user_id = session['userid']

        # Fetch learner information
        learner_info = get_learner_info(user_id)
        goal_info = get_goal_info(user_id)

        return render_template('menuL.html', learner=learner_info, goal = goal_info)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/select_current_language', methods=['GET', 'POST'])
def select_current_language():
    if request.method == 'POST':
        language_name = request.form.get('language')
        level = request.form.get('level')

        # Obtain Language_id based on language name and level
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT Language_id FROM Language WHERE Language_name = %s AND Language_level = %s',
            (language_name, level)
        )
        language_data = cursor.fetchone()

        if language_data:
            language_id = language_data['Language_id']

            # Insert data into Current_Level table
            cursor.execute(
                'INSERT INTO Current_Level (Language_id, U_id) VALUES (%s, %s)',
                (language_id, session['userid'])
            )
            mysql.connection.commit()

            # You may want to redirect to another page or display a success message
            return redirect(url_for('menuL'))
        else:
            # Handle the case where the language was not found
            flash('Selected language not found.')

            # You may want to redirect to another page or display a success message
            return redirect(url_for('menuL'))

    # Fetch languages from the Language table
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT DISTINCT Language_name FROM Language')
    languages = [language['Language_name'] for language in cursor.fetchall()]

    return render_template('select_current_language.html', languages=languages)

def update_goal_language(user_id, language_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Check if the goal language already exists for the user
    cursor.execute(
        'SELECT * FROM Goal_Level WHERE U_id = %s AND Language_id = %s',
        (user_id, language_id)
    )
    
    goal_language_data = cursor.fetchone()

    if not goal_language_data:
        # Insert data into Goal_Level table
        cursor.execute(
            'INSERT INTO Goal_Level (Language_id, U_id) VALUES (%s, %s)',
            (language_id, user_id)
        )
        mysql.connection.commit()
        return True  # Success
    else:
        return False  # Language already selected as a goal

@app.route('/select_goal_language', methods=['GET', 'POST'])
def select_goal_language():
    if request.method == 'POST':
        language_name = request.form.get('language')
        level = request.form.get('level')

        # Obtain Language_id based on language name and level
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT Language_id FROM Language WHERE Language_name = %s AND Language_level = %s',
            (language_name, level)
        )
        language_data = cursor.fetchone()

        if language_data:
            language_id = language_data['Language_id']

            # Update Goal_Level table
            success = update_goal_language(session['userid'], language_id)

            if success:
                # Redirect to another page or display a success message
                return redirect(url_for('menuL'))
            else:
                # Handle the case where the language is already a goal language
                flash('Selected language is already a goal language.')

                # Redirect to another page or display a message
                return redirect(url_for('menuL'))
        else:
            # Handle the case where the language was not found
            flash('Selected language not found.')

            # Redirect to another page or display a message
            return redirect(url_for('menuL'))

    # Fetch languages from the Language table
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT DISTINCT Language_name FROM Language')
    languages = [language['Language_name'] for language in cursor.fetchall()]

    return render_template('select_goal_language.html', languages=languages)

@app.route('/menuT', methods =['GET', 'POST'])
def menuT():
    return render_template('menuT.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
