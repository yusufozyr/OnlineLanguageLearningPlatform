
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'projectdb'

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
        cursor.execute('SELECT * FROM User WHERE U_id = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['U_id']
            session['username'] = user['U_id']
            message = 'Logged in successfully!'
            return redirect(url_for('menuL'))
        else:
            message = 'Please enter correct User Name and Password !'
    return render_template('login.html', message = message)

app.route('/menuL', methods =['GET', 'POST'])
def menuL():
    return render_template('login.html', message = message)








# @app.route('/tasks', methods=['GET', 'POST'])
# def tasks():
#     if 'loggedin' in session:
#         student_id = session['userid']
        
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT c.cid, c.cname, c.quota, c.gpa_threshold FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s', (student_id,))
#         internship_applications = cursor.fetchall()
        
#         cursor.execute('SELECT COUNT(*) AS count FROM apply WHERE sid = %s', (student_id,))
#         application_count = cursor.fetchone()
        
#         return render_template('tasks.html', internship_applications=internship_applications, application_count=application_count)
#     return redirect(url_for('login'))
# @app.route('/apply_internship', methods=['GET', 'POST'])
# def apply_internship():
#     success_message = None
#     error_message = None

#     if request.method == 'POST':
#         student_id = session['userid']
#         company_id = request.form['company_id']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         query = """
#         SELECT c.cid
#         FROM company c
#         LEFT JOIN apply a ON c.cid = a.cid AND a.sid = %s
#         WHERE a.sid IS NULL
#             AND (c.quota > (SELECT COUNT(*) FROM apply ap WHERE ap.cid = c.cid) OR c.quota IS NULL)
#             AND (c.gpa_threshold <= (SELECT gpa FROM student s WHERE s.sid = %s) OR c.gpa_threshold IS NULL)
#         """
#         cursor.execute(query, (student_id, student_id))
#         applicable_companies = [result['cid'] for result in cursor.fetchall()]

#         if company_id not in applicable_companies:
#             error_message = f'Company ID {company_id} is not applicable for you.'
#         else:
#             insert_query = "INSERT INTO apply (sid, cid) VALUES (%s, %s)"
#             cursor.execute(insert_query, (student_id, company_id))
#             mysql.connection.commit()

#             success_message = 'Application submitted successfully!'
#             return redirect(url_for('tasks'))
#     student_id = session['userid']
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     query = """
#     SELECT c.cid, c.cname
#     FROM company c
#     LEFT JOIN apply a ON c.cid = a.cid AND a.sid = %s
#     WHERE a.sid IS NULL
#         AND (c.quota > (SELECT COUNT(*) FROM apply ap WHERE ap.cid = c.cid) OR c.quota IS NULL)
#         AND (c.gpa_threshold <= (SELECT gpa FROM student s WHERE s.sid = %s) OR c.gpa_threshold IS NULL)
#     """
#     cursor.execute(query, (student_id, student_id))
#     available_companies = cursor.fetchall()

#     return render_template('application_form.html', available_companies=available_companies, success_message=success_message, error_message=error_message)


# @app.route('/cancel_application/<cid>', methods=['GET'])
# def cancel_application(cid):
#     if 'loggedin' in session:
#         student_id = session['userid']
        
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('DELETE FROM apply WHERE sid = %s AND cid = %s', (student_id, cid))
#         mysql.connection.commit()
        
#         if cursor.rowcount > 0:
#             return redirect(url_for('tasks', success_message='Application canceled successfully'))
#         else:
#             return redirect(url_for('tasks', error_message='Failed to cancel the application'))

#     return redirect(url_for('login'))

# @app.route('/application_summary', methods=['GET'])
# def application_summary():
#     if 'loggedin' in session:

#         student_id = session['userid']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT c.cid, c.cname, c.quota, c.gpa_threshold FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s ORDER BY c.quota DESC', (student_id,))
#         desc = cursor.fetchall()

#         cursor.execute('SELECT MAX(c.gpa_threshold) AS max_gpa_threshold, MIN(c.gpa_threshold) AS min_gpa_threshold '
#                        'FROM company c JOIN apply a ON c.cid = a.cid WHERE a.sid = %s', (student_id,))
#         gpa_thresholds = cursor.fetchone()

#         cursor.execute('SELECT c.cid, c.cname '
#                        'FROM company c JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s AND c.gpa_threshold = %s', (student_id, gpa_thresholds['max_gpa_threshold']))
#         max_threshold_company = cursor.fetchone()

#         cursor.execute('SELECT c.cid, c.cname '
#                        'FROM company c JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s AND c.gpa_threshold = %s', (student_id, gpa_thresholds['min_gpa_threshold']))
#         min_threshold_company = cursor.fetchone()

#         cursor.execute('SELECT c.city, COUNT(c.cid) AS application_count '
#                        'FROM company c JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s GROUP BY c.city', (student_id,))
#         city_count = cursor.fetchall()

#         cursor.execute('SELECT c.cname FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s ORDER BY c.quota DESC LIMIT 1', (student_id,))
#         company_with_max_quota = cursor.fetchone()

#         # Fetch the company with the minimum quota
#         cursor.execute('SELECT c.cname FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s ORDER BY c.quota ASC LIMIT 1', (student_id,))
#         company_with_min_quota = cursor.fetchone()
        
#         return render_template('application_summary.html',
#                                desc=desc,
#                                gpa_thresholds=gpa_thresholds,
#                                max_threshold_company=max_threshold_company,
#                                min_threshold_company=min_threshold_company,
#                                city_count=city_count,
#                                company_with_max_quota=company_with_max_quota,
#                                company_with_min_quota=company_with_min_quota)
#     return redirect(url_for('login'))


# @app.route('/logout')
# def logout():
#     if 'loggedin' in session:
#         session.pop('loggedin', None)
#         session.pop('userid', None)
#         session.pop('username', None)
#         session.pop('email', None)
#     return redirect(url_for('login'))
# @app.route('/analysis', methods =['GET', 'POST'])


# def analysis():
#     return "Analysis page"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
